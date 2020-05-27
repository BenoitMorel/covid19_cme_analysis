/*
    Genesis - A toolkit for working with phylogenetic data.
    Copyright (C) 2014-2020 Lucas Czech

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
    Lucas Czech <lucas.czech@h-its.org>
    Exelixis Lab, Heidelberg Institute for Theoretical Studies
    Schloss-Wolfsbrunnenweg 35, D-69118 Heidelberg, Germany
*/

#include "genesis/genesis.hpp"

using namespace genesis;
using namespace genesis::sequence;
using namespace genesis::utils;

#include <string>
#include <unordered_map>
#include <vector>
#include <sstream>
#include <string>
#include <fstream>

int main( int argc, char** argv )
{
    // Activate logging.
    utils::Logging::log_to_stdout();
    utils::Logging::details.time = true;

    // Get the files from command line
    if (argc != 4) {
        throw std::runtime_error(
            std::string( "Usage: " ) + argv[0] + " <input-msa> <output-fasta> <output-json>"
        );
    }
    auto const infile = std::string( argv[1] );
    auto const outfile = std::string( argv[2] );
    auto const outfilejson = std::string( argv[3] );

    LOG_INFO << "Specified: infile = " << infile;

    // Prepare duplicate map, from sequences to all labels that have that sequence
    std::unordered_map<std::string, std::vector<std::string>> seq_map;

    // Read the file
    LOG_INFO << "Started";
    auto fasta_in = FastaInputIterator( from_file( infile ));
    size_t cnt = 0;
    while( fasta_in ) {
        auto seq = *fasta_in;
        replace_characters( seq, "Nn", '-' );

        if( seq.sites().empty() || seq.label().empty() ) {
            throw std::runtime_error( "Invalid sequences with empty label or sites." );
        }

        // normal case
        seq_map[ seq.sites() ].push_back( seq.label() );
        ++cnt;

        ++fasta_in;
    }
    LOG_INFO << "Found " << cnt << " sequences, thereof " << seq_map.size() << " unique.";

    // Write out the reduced fasta file
    FastaOutputIterator fasta_out{ to_file(outfile) };
    for( auto const& seq : seq_map ) {
        auto const tmp_seq = Sequence( seq.second[0], seq.first );
        fasta_out << tmp_seq;
    }

    // Write out a json file with the mapping. We write the name that is used in the fasta file
    // first as an object key, and then all labels (including the one from the fasta) as a list.
    // This makes it easy to re-attach later.
    JsonDocument doc = JsonDocument::object();
    for( auto const& seq : seq_map ) {
        if( seq.second.size() > 1 ) {
            auto arr = JsonDocument::array();
            for( size_t i = 0; i < seq.second.size(); ++i ) {
                arr.push_back( seq.second[i] );
            }
            doc[ seq.second[0] ] = arr;
        }
    }
    JsonWriter().write( doc, to_file( outfilejson ));

    LOG_INFO << "Finished";
    return 0;
}
