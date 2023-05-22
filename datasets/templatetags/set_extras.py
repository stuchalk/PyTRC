""" template tags, filters etc. for datasets """
from django import template
register = template.Library()


def df2htmlhdrs(df):
    """ dataframe to HTML headers """
    html = "<tr>"
    for col in df.columns:
        html += f"<th>{col}</th>"
        html += "</tr>"
    return html


def df2htmlrows(df):
    """ dataframe to HTML rows """
    html = ""
    for row in df.values:
        row_html = "<tr>"
        for value in row:
            row_html += f"<td>{value}</td>"
            row_html += "</tr>"
        html += row_html
    return html


def getbykey(value, key):
    """ get the value from a dictionary key"""
    return value[key]


register.filter("df2htmlhdrs", df2htmlhdrs)
register.filter("df2htmlrows", df2htmlrows)
register.filter("getbykey", getbykey)
