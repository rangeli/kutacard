#!/usr/bin env python3

# Generates C++ header file containing table to convert
# from Shift-JIS to UTF-8


def process_shiftjis_table(path):
    table = []
    with open(path, 'r') as f:
        for line in f.readlines():
            if line[0] == '#':
                continue

            tokens = line.split('\t', 3)
            tokens = [token.strip() for token in tokens]
            tokens[2] = tokens[2].lstrip('# ').lower()
            table.append((tokens[0], tokens[1], tokens[2]))
    return table


def generate_code(table):
    template = """\
#ifndef SHIFTJIS_SHIFTJIS_TABLE_H
#define SHIFTJIS_SHIFTJIS_TABLE_H

// THIS FILE WAS AUTOGENERATED USING SHIFTJIS-GENERATOR.PY

#include <string>
#include <unordered_map>

namespace shiftjis
{{
static const std::unordered_map<uint16_t, char const*> Utf8ConversionTable = {{
{elements}
}};
}}

#endif // SHIFTJIS_SHIFTJIS_TABLE_H
"""
    elements = str()
    for (shift_char, utf_char, comment) in table[:-1]:
        elements += '  {{{shift_char}, \"\\u{utf_char}\"}}, // {comment}\n'.format(
            shift_char=shift_char, utf_char=utf_char.replace('0x', ''), comment=comment)

    # Last item needs to be slightly different
    elements += '  {{{shift_char}, \"\\u{utf_char}\"}}  // {comment}'.format(
            shift_char=table[-1][0], utf_char=table[-1][1].replace('0x', ''), comment=table[-1][2])
    return template.format(elements=elements)


if __name__ == '__main__':
    table = process_shiftjis_table('SHIFTJIS.TXT')
    code = generate_code(table)
    with open('../include/shiftjis_table.h', 'w') as output:
        output.write(code)
