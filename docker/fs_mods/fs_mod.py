import fileinput

with fileinput.FileInput(files=('/FairShip/CMakeLists.txt'), inplace=True) as input:
	for line in input:
	    if "add_subdirectory (passive)" in line:
	        line=line.replace(line,line+"add_subdirectory (fluxDet)\n")
	    print (line, end='')
	input.close()

with fileinput.FileInput(files=('/FairShip/passive/ShipMuonShield.cxx'), inplace=True) as input:
        for line in input:
            if "Double_t LE = 10. * m, floor = 5. * m;" in line:
                line=line.replace("5.", "4.2")
            print (line, end='')
        input.close()


with fileinput.FileInput(files=('/FairShip/python/shipRoot_conf.py'), inplace=True) as input:
	for line in input:
	    if "ROOT.gSystem.Load('libShipPassive')" in line:
	        line=line.replace(line,line+"   ROOT.gSystem.Load('libfluxDet')\n")
	    print (line, end='') 
	input.close()

with fileinput.FileInput(files=('/FairShip/shipdata/ShipDetectorList.h'), inplace=True) as input:
	for line in input:
	    if "DetectorId" in line:
	        line=line.replace("kVETO", "kVETO, kfluxDet")
	    print (line, end='') 
	input.close()

with fileinput.FileInput(files=('/FairShip/passive/ShipMuonShield.h'), inplace=True) as input:
	for line in input:
	    if "Int_t  fDesign;" in line:
	        line=line.replace(line, line + "   void PreTrack();\n  Bool_t ProcessHits(FairVolume*);\n")
	    print (line, end='') 
	input.close()

with fileinput.FileInput(files=('/FairShip/passive/ShipMuonShield.cxx'), inplace=True) as input:
	for line in input:
	    if "iostream" in line:
	        line=line.replace(line, line + '#include "TVirtualMC.h"\n')
	    print (line, end='') 
	input.close()

with fileinput.FileInput(files=('/FairShip/passive/ShipMuonShield.cxx'), inplace=True) as input:
	for line in input:
	    if "tShield->AddNode(magF, " in line:
	        line=line.replace(line, 'AddSensitiveVolume(magF);\n' + line + '\n')
	    print (line, end='') 
	input.close()


with fileinput.FileInput(files=('/FairShip/passive/ShipMuonShield.cxx'), inplace=True) as input:
	for line in input:
	    if "tShield->AddNode(magF[i]" in line:
	        line=line.replace(line, 'AddSensitiveVolume(magF[i]);\n' + line + '\n')
	    print (line, end='') 
	input.close()

#new_line = """void ShipMuonShield::PreTrack(){
#    if (TMath::Abs(gMC->TrackPid())!=13){
#        gMC->StopTrack();
#    }
#}
#Bool_t   ShipMuonShield::ProcessHits(FairVolume* vol){return kTRUE;};\n
#"""
new_line = """void ShipMuonShield::Reset()
{

}
TClonesArray* ShipMuonShield::GetCollection(Int_t iColl) const
{
 return NULL;
}
void ShipMuonShield::Register()
{}
void ShipMuonShield::PreTrack(){
    if (TMath::Abs(gMC->TrackPid())!=13){
        gMC->StopTrack();
    }
}
Bool_t   ShipMuonShield::ProcessHits(FairVolume* vol){return kTRUE;};\n
"""
with fileinput.FileInput(files=('/FairShip/passive/ShipMuonShield.cxx'), inplace=True) as input:
	for line in input:
	    if "ClassImp(ShipMuonShield)" in line:
	        line=line.replace(line, new_line + line + '\n')
	    print (line, end='') 
	input.close()

with fileinput.FileInput(files=('/FairShip/passive/ShipMuonShield.h'), inplace=True) as input:
        for line in input:
            if "FairModule" in line:
                line=line.replace("FairModule", "FairDetector")
            print (line, end='')
        input.close()

with fileinput.FileInput(files=('/FairShip/passive/ShipMuonShield.cxx'), inplace=True) as input:
        for line in input:
            if "FairModule" in line:
                line=line.replace("FairModule", "FairDetector")
            print (line, end='')
        input.close()

newLine = """virtual void   Register();
virtual TClonesArray* GetCollection(Int_t iColl) const ;
virtual void   Reset();"""

with fileinput.FileInput(files=('/FairShip/passive/ShipMuonShield.h'), inplace=True) as input:
        for line in input:
            if "Int_t  fDesign;" in line:
                line=line.replace(line, newLine + line +'\n')
            print (line, end='')
        input.close()


