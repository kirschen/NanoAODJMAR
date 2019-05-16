import FWCore.ParameterSet.Config as cms
from  PhysicsTools.NanoAOD.common_cff import *





finalJetsAK8Constituents = cms.EDProducer("PatJetConstituentPtrSelector",
                                            src = cms.InputTag("updatedJetsAK8"),
                                            cut = cms.string("pt > 170.0")
                                            )
genJetsAK8Constituents = cms.EDProducer("GenJetPackedConstituentPtrSelector",
                                            src = cms.InputTag("slimmedGenJetsAK8"),
                                            cut = cms.string("pt > 100.0")
                                            )



##################### Tables for final output and docs ##########################
finalJetsAK8ConstituentsTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("finalJetsAK8Constituents", "constituents"),
    cut = cms.string(""), #we should not filter after pruning
    name= cms.string("PFCandsAK8"),
    doc = cms.string("interesting gen particles from AK8 jets"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table for the AK8 constituents
    variables = cms.PSet(CandVars,
                            puppiWeight = Var("puppiWeight()", float, doc="Puppi weight",precision=10),
                            puppiWeightNoLep = Var("puppiWeightNoLep()", float, doc="Puppi weight removing leptons",precision=10),
    )
)

##################### Tables for final output and docs ##########################
genJetsAK8ParticleTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("genJetsAK8Constituents", "constituents"),
    cut = cms.string(""), #we should not filter after pruning
    name= cms.string("GenPartAK8"),
    doc = cms.string("interesting gen particles from AK8 jets"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table for the AK8 constituents
    variables = cms.PSet(CandVars
    )
)

jetReclusterSequence = cms.Sequence(finalJetsAK8Constituents)
jetReclusterMCSequence = cms.Sequence(genJetsAK8Constituents)
jetReclusterTable = cms.Sequence(finalJetsAK8ConstituentsTable)
jetReclusterMCTable = cms.Sequence(genJetsAK8ParticleTable)

from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJets
pfCHSCandsNew = cms.EDFilter("CandPtrSelector", src = cms.InputTag("packedPFCandidates"), cut = cms.string("fromPV"))

ak4PFCHSreco = ak4PFJets.clone(src = 'pfCHSCandsNew', jetPtMin=15., rParam       = cms.double(0.4)) 
ak4jetTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("ak4PFCHSreco"),
    cut = cms.string(""), #we should not filter on cross linked collections
    name = cms.string("Jetak4PFCHS"),
    doc  = cms.string("Jetak4PFCHS, i.e. ak4 PFJets CHS (plain reco, i.e. without JEC applied)"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table for the jets
    variables = cms.PSet(P4Vars,
        area = Var("jetArea()", float, doc="jet catchment area, for JECs",precision=10),
    )
)
ak4jetTable.variables.pt.precision=10

ak7PFCHSreco = ak4PFJets.clone(src = 'pfCHSCandsNew', jetPtMin=50., rParam       = cms.double(0.7)) 
ak7jetTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("ak7PFCHSreco"),
    cut = cms.string(""), #we should not filter on cross linked collections
    name = cms.string("Jetak7PFCHS"),
    doc  = cms.string("Jetak7PFCHS, i.e. ak7 PFJets CHS (plain reco, i.e. without JEC applied)"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table for the jets
    variables = cms.PSet(P4Vars,
        area = Var("jetArea()", float, doc="jet catchment area, for JECs",precision=10),
    )
)
ak7jetTable.variables.pt.precision=10

ak8PFCHSreco = ak4PFJets.clone(src = 'pfCHSCandsNew', jetPtMin=50., rParam       = cms.double(0.8)) 
ak8jetTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("ak8PFCHSreco"),
    cut = cms.string(""), #we should not filter on cross linked collections
    name = cms.string("Jetak8PFCHS"),
    doc  = cms.string("Jetak8PFCHS, i.e. ak8 PFJets CHS (plain reco, i.e. without JEC applied)"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table for the jets
    variables = cms.PSet(P4Vars,
        area = Var("jetArea()", float, doc="jet catchment area, for JECs",precision=10),
    )
)
ak8jetTable.variables.pt.precision=10



ak4Sequence = cms.Sequence(ak4PFCHSreco+ak4jetTable)
ak7Sequence = cms.Sequence(ak7PFCHSreco+ak7jetTable)
ak8Sequence = cms.Sequence(ak8PFCHSreco+ak8jetTable)

nanoJetCollections = cms.Sequence(pfCHSCandsNew+ak4Sequence+ak7Sequence+ak8Sequence)



from  PhysicsTools.NanoAOD.common_cff import *
ak4jetMiniAODTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("selectedPatJetsAK4PFCHS"),
    cut = cms.string(""), #we should not filter on cross linked collections
    name = cms.string("PATJetsNewAK4PFCHS"),
    doc  = cms.string("PATJetsNewAK4PFCHS, i.e. ak4 PFJets CHS (a la miniAOD, so should be the same thing as standard nanoAOD...)"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table for the jets
    variables = cms.PSet(P4Vars,
        area = Var("jetArea()", float, doc="jet catchment area, for JECs",precision=10),
    )
)
ak4jetMiniAODTable.variables.pt.precision=10


nanoJetCollections+=cms.Sequence(ak4jetMiniAODTable)
