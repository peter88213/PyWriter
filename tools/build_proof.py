""" Build python scripts for the PyWriter "proofread" distributions.
        
In order to distribute single scripts without dependencies, 
this script "inlines" all modules imported from the pywriter package.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import inliner

SRC = '../src/'
BUILD = '../test/'


def main():
    os.chdir(SRC)
    inliner.run('proofdocx.pyw', BUILD + 'yw_proof_docx.pyw', 'pywriter')
    inliner.run('proofodt.pyw', BUILD + 'yw_proof_odt.pyw', 'pywriter')
    inliner.run('proofhtml.pyw', BUILD + 'yw_proof_html.pyw', 'pywriter')
    print('Done.')


if __name__ == '__main__':
    main()
