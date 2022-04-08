#!/bin/bash
mkdir -p $AZURE_OUTPUT_DATA_URI
alienv -w /sw setenv  FairShip/latest  -c /bin/bash  -c "python run_opt.py --FastMuon --processMiniShield  --MuonBack -f muon_input/reweighted_input_test.root --optParams \"$PARAMS\" --nEvents $nEvents --firstEvent $first_event --output $AZURE_OUTPUT_DATA_URI   --muShieldDesign 8 -g /ship/shield_files/geometry/shield_params.root"
