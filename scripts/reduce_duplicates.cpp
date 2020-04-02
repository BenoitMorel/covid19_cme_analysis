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

int main( int argc, char** argv )
{
    // Activate logging.
    utils::Logging::log_to_stdout();
    utils::Logging::details.time = true;

    // Get the files from command line
    if (argc != 2) {
        throw std::runtime_error(
            "Need to provide a fasta file.\n"
        );
    }
    auto const infile = std::string( argv[1] );

    // Prepare duplicate map, from sequences to all labels that have that sequence
    std::unordered_map<std::string, std::vector<std::string>> seq_map;

    // Read the file
    LOG_INFO << "Started";
    auto fasta_in = FastaInputIterator( from_file( infile ));
    size_t cnt = 0;
    while( fasta_in ) {
        if( fasta_in->sites().empty() || fasta_in->label().empty() ) {
            throw std::runtime_error( "Invalid sequences with empty label or sites." );
        }

        seq_map[ fasta_in->sites() ].push_back( fasta_in->label() );
        ++cnt;
        ++fasta_in;
    }
    LOG_INFO << "Found " << cnt << " sequences, thereof " << seq_map.size() << " unique.";

    // Prepare a nice output filename
    std::string outfile_base = infile;
    auto const ext = file_extension( infile );
    if( ext == "fa" || ext == "fas" || ext == "fasta" ) {
        outfile_base = file_filename( outfile_base );
    }

    // Write out the reduced fasta file
    std::ofstream out_stream;
    file_output_stream( outfile_base + ".reduced.fasta", out_stream );
     FastaOutputIterator fasta_out{ out_stream };
    for( auto const& seq : seq_map ) {
        auto const tmp_seq = Sequence( seq.second[0], seq.first );
        fasta_out = tmp_seq;
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
    JsonWriter().to_file( doc, outfile_base + ".reduced.json" );

    LOG_INFO << "Finished";
    return 0;
}
