import ROOT
import tdrstyle
import math
import os

import sys
for arg in sys.argv: 
    print arg

inputFolder = sys.argv[1]
jetRadius = sys.argv[2]


tdrstyle.setTDRStyle()
ROOT.gStyle.SetPadRightMargin(0.15)
ROOT.gStyle.SetPalette(1)

def makeCanvas(hists, tags):
    colors = [1,2,4,5,6,7,8]

    if hists[0].GetName() == "h_jpres_pf":            
        leg = ROOT.TLegend(0.2,0.75,0.6,0.9)
    else:
        leg = ROOT.TLegend(0.2,0.6,0.6,0.9)
    leg.SetHeader("Jet radius="+jetRadius)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    tmax = -999

    for i in range(len(hists)):
        leg.AddEntry(hists[i],tags[i],'l')
        if hists[i].GetMaximum() > tmax:
            tmax = hists[i].GetMaximum()
            
    c = ROOT.TCanvas("c","c",1000,800)
    for i in range(len(hists)):
        if i == 0:
            hists[i].DrawNormalized('hist')
        else: 
            hists[i].SetLineColor( colors[i] )
            hists[i].DrawNormalized('histsames')

        hists[0].DrawNormalized('histsames')
        leg.Draw()

#        hists[0].SetMinimum(0)

        if hists[0].GetName() == "h_jeta_gen" or hists[0].GetName() == "h_jpres_pf" or hists[0].GetName() == "h_jphi_gen":
            hists[0].SetMaximum(tmax*1.7)
#        if hists[0].GetName() == "h_jmass_gen":
#            c.SetLogy(1)
        else:
            hists[0].SetMaximum(tmax*1.3)

        c.SaveAs(directory+"/radius"+jetRadius+"_"+hists[0].GetName()+".pdf")
        c.SaveAs(directory+"/radius"+jetRadius+"_"+hists[0].GetName()+".png")

## tin, PF, gen
def getHists(tin,tin1,tin2,postfix):
	h_je       = ROOT.TH1F("h_je"+postfix,"; jet energy; N",100,0,3000);
	h_jpt      = ROOT.TH1F("h_jpt"+postfix,"; pT; N",100,0,3000)
	h_jp       = ROOT.TH1F("h_jp"+postfix,"; p; N",100,0,3000)

        

	h_jeta     = ROOT.TH1F("h_jeta"+postfix,"; eta; N",80,-2,2)
	h_jphi     = ROOT.TH1F("h_jphi"+postfix,"; phi; N",50,0,2*3.15)
	h_jmass    = ROOT.TH1F("h_jmass"+postfix,"; mass; N",50,0,200)
	h_jmass_sd = ROOT.TH1F("h_jmass_sd"+postfix,"; soft drop mass (#beta = 0); N",50,0,200)

#        print tin.GetEntriesFast()
	for i in range(tin.GetEntriesFast()):
		tin.GetEntry(i)
                tin1.GetEntry(i)
                tin2.GetEntry(i)
#                print len(tin1.jpt), len(tin2.jpt)
                for j in range(len(tin1.jpt)):
                    if tin1.jisleptag[j] == 0: 
#                    print "j=", j
                        for k in range(len(tin2.jpt)):
                            if tin2.jisleptag[k] == 0:
                            #                        print "k=", k
                                dr = math.sqrt( (tin1.jphi[j]-tin2.jphi[k])*(tin1.jphi[j]-tin2.jphi[k]) + (tin1.jeta[j]-tin2.jeta[k])*(tin1.jeta[j]-tin2.jeta[k]) )
                               #                        print "dr=", dr
                                if dr < 0.01: 
                                    for n in range(len(tin.jpt)):
                                        drpf = math.sqrt( (tin1.jphi[j]-tin.jphi[n])*(tin1.jphi[j]-tin.jphi[n]) + (tin1.jeta[j]-tin.jeta[n])*(tin1.jeta[j]-tin.jeta[n]) )
                                        if drpf < 0.4 and tin.jisleptag[n]==0:
                                            h_je.Fill( tin.je[n] )
                                            h_jpt.Fill( tin.jpt[n] )
                                            h_jp.Fill( tin.jp[n] )				
                                            h_jeta.Fill( tin.jeta[n] )
                                            h_jphi.Fill( tin.jphi[n] )
                                            h_jmass.Fill( tin.jmass[n] )
                                            h_jmass_sd.Fill( tin.jmass_sd[n] )	

#        print h_je.GetEntries()
        hists = []
	hists.append( h_je )
	hists.append( h_jpt )
	hists.append( h_jp )
	hists.append( h_jeta )
	hists.append( h_jphi )
	hists.append( h_jmass )
	hists.append( h_jmass_sd )
	return hists


def MCinfo(tin):

    h_mzp = ROOT.TH1F("h_mh2","; H2 mass; N",100,0,10000);
    h_mzp.SetNdivisions(5);
    for i in range(tin.GetEntriesFast()):
        tin.GetEntry(i);
        h_mzp.Fill(tin.gen_mZp);
    return h_mzp;


## tin, PF, gen

def GetResolutions(tin,tin1,tin2,pf):

	h_jpres = ROOT.TH1F("h_jpres_"+pf, "; (P - PGEN)/PGEN; au", 50,-1,1)

	for i in range(tin.GetEntriesFast()):
		tin1.GetEntry(i)
		tin2.GetEntry(i)
                tin.GetEntry(i)
		for j in range(len(tin1.jpt)):
                    if tin1.jisleptag[j] == 0: 
                        for k in range(len(tin2.jpt)):
                            if tin2.jisleptag[k] == 0:
                                dr = math.sqrt( (tin1.jphi[j]-tin2.jphi[k])*(tin1.jphi[j]-tin2.jphi[k]) + (tin1.jeta[j]-tin2.jeta[k])*(tin1.jeta[j]-tin2.jeta[k]) )
                                if dr < 0.01: 
                                    for n in range(len(tin.jpt)):
                                        drpf = math.sqrt( (tin1.jphi[j]-tin.jphi[n])*(tin1.jphi[j]-tin.jphi[n]) + (tin1.jeta[j]-tin.jeta[n])*(tin1.jeta[j]-tin.jeta[n]) )
                                        if(drpf < 0.4 and tin.jisleptag[n]==0):
                                            h_jpres.Fill( (tin.jp[n] - tin2.jp[k])/tin2.jp[k] )				
                                                    
        return h_jpres

if __name__ == '__main__':

        directory = 'plots_radius' + jetRadius
        if not os.path.exists(directory):
                os.makedirs(directory)
        else:
                print 'the directory already exists! rememebr to clean up your work area'
                quit()

        fa = ROOT.TFile(inputFolder+"/radius"+jetRadius+"_of_PanPFA.root")
        tg = fa.Get("tGEN")
        tg_charged = fa.Get("tGEN_charged")
        tg_nonu    = fa.Get("tGEN_nonu")
        ta = fa.Get("tPFA")
        tc = fa.Get("tcalo")
        tt = fa.Get("ttrack")
        tmc = fa.Get("tMC")

        print "Getting hists..."
        hg = getHists(tg,ta,tg,'_gen')
        hg_charged = getHists(tg_charged,ta,tg,'_gen_charged')
        hg_nonu    = getHists(tg_nonu,ta,tg,'_gen_nonu')
        ha = getHists(ta,ta,tg,'_PF')
        ht = getHists(tt,ta,tg,'_trk')	
        hc = getHists(tc,ta,tg,'_calo')

        for i in range(len(ha)):
            makeCanvas( [hg[i],hg_charged[i],hg_nonu[i],ha[i],ht[i], hc[i]], ['gen','gen_charged','gen_nonu','pf','track (associated) ','calo (associated)'] )

        hmc = MCinfo(tmc);
        makeCanvas([hmc],['particlelevel'])

        hres_pf    = GetResolutions(ta,ta,tg, "pf" )
        hres_track = GetResolutions(tt,ta,tg, "track")
        hres_cal   = GetResolutions(tc,ta,tg, "calo" )
        makeCanvas( [hres_pf, hres_track, hres_cal], ['pf','track (associated)', 'calo (associated)'] )





