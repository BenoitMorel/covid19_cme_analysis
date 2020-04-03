/*
    Copyright (C) 2018 Pierre Barbera

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Contact:
    Pierre Barbera <pierre.barbera@h-its.org>
    Exelixis Lab, Heidelberg Institute for Theoretical Studies
    Schloss-Wolfsbrunnenweg 35, D-69118 Heidelberg, Germany
*/

#include "genesis/genesis.hpp"

#include <fstream>
#include <string>
#include <algorithm>

using namespace genesis;
using namespace genesis::sequence;
using namespace genesis::utils;

bool contains(std::vector<std::string> const& vec, std::string const& s) {
    return std::find(std::begin(vec), std::end(vec), s) != std::end(vec);
}

int main( int argc, char** argv )
{

    std::vector<std::string> const sequence_types = {"fasta", "phylip", "interleaved_phylip"};

    // Check if the command line contains the right number of arguments.
    if (argc != 5) {
        throw std::runtime_error(
            std::string( "Usage: " ) + argv[0] + " <in type> <out type> <in-file> <out-file>"
        );
    }

    // Get command line stuff.
    auto in_type = to_lower(std::string( argv[1] ));
    auto out_type = to_lower(std::string( argv[2] ));
    auto in_file = std::string( argv[3] );
    auto out_file = std::string( argv[4] );

    // sequence files
    if ( contains( sequence_types, in_type ) ) {
        SequenceSet set;
        if ( in_type == "fasta" ) {
            FastaReader()
                .read( from_file( in_file ), set );
        } else if ( in_type == "phylip" ) {
            PhylipReader()
                .read( from_file( in_file ), set );
        } else if ( in_type == "interleaved_phylip" ) {
            PhylipReader().mode(PhylipReader::Mode::kInterleaved)
                .read( from_file( in_file ), set );
        }

        if ( out_type == "fasta") {
            FastaWriter().to_file( set, out_file );
        } else if ( out_type == "phylip") {
            PhylipWriter().line_length(0).to_file( set, out_file );
        } else if ( out_type == "interleaved_phylip") {
            //PhylipWriter().mode()
            //    .to_stream( set, std::cout );
               throw std::runtime_error{std::string("output type not supported: '") + out_type + "'"};
        } else {
            throw std::runtime_error{std::string("output type not supported: '") + out_type + "'"};
        }

    } else {
        throw std::runtime_error{std::string("input type not supported: '") + in_type + "'"};
    }

    return 0;
}