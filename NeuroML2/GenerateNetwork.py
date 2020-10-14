from neuromllite import Network, Cell, Population, Synapse, RectangularRegion, RandomLayout 
from neuromllite import Projection, RandomConnectivity, OneToOneConnector, Simulation

from neuromllite.NetworkGenerator import check_to_generate_or_run
from neuromllite.sweep.ParameterSweep import *

import sys


def generate():
    
    dt = 0.015
    simtime = 600
    
    ################################################################################
    ###   Build new network

    net = Network(id='MaexDeSchutter1998')
    net.notes = 'Example 7: MaexDeSchutter1998'
    net.temperature = 32.0 # degC
    
    net.parameters = {'num_MF':              12,
                      'num_GrC':             75,
                      'num_Gol':             4,
                      'mf_rate':             50,
                      'weight_mf_grc_ampa':  6,
                      'weight_mf_grc_nmda':  4,
                      'weight_grc_gol':      .6,
                      'weight_gol_grc':      45}

    grc = Cell(id='Granule_98', neuroml2_source_file='Granule_98.cell.nml')
    net.cells.append(grc)
    gol = Cell(id='Golgi_98', neuroml2_source_file='Golgi_98.cell.nml')
    net.cells.append(gol)

    poisson_input = Cell(id='poisson_input', pynn_cell='SpikeSourcePoisson')
    poisson_input.parameters = { 'rate':       'mf_rate',
                             'start':      0,
                             'duration':   1e9}
    net.cells.append(poisson_input)
    

    r1 = RectangularRegion(id='GranuleCellLayer', x=0,y=0,z=0,width=1000,height=100,depth=1000)
    net.regions.append(r1)

    pop_grc = Population(id='GrCs', 
                    size='num_GrC', 
                    component=grc.id, 
                    properties={'color':'.8 0 0'},
                    random_layout = RandomLayout(region=r1.id))
    net.populations.append(pop_grc)

    pop_gol = Population(id='Gols', 
                    size='num_Gol', 
                    component=gol.id, 
                    properties={'color':'0 0.8 0'},
                    random_layout = RandomLayout(region=r1.id))
    net.populations.append(pop_gol)
                 
    pop_mf = Population(id='MFs', 
                           size='num_MF', 
                           component=poisson_input.id, 
                           properties={'color':'0 0 0.8', 'radius':3},
                           random_layout = RandomLayout(region=r1.id))
    net.populations.append(pop_mf)
    

    
    mf_ampa_syn = Synapse(id='MF_AMPA', 
                          neuroml2_source_file='MF_AMPA.synapse.nml')
    net.synapses.append(mf_ampa_syn)
    
    nmda_syn = Synapse(id='NMDA', 
                          neuroml2_source_file='NMDA.synapse.nml')
    net.synapses.append(nmda_syn)
    
    ampa_gr_gol_syn = Synapse(id='AMPA_GranGol', 
                          neuroml2_source_file='AMPA_GranGol.synapse.nml')
    net.synapses.append(ampa_gr_gol_syn)
    
    gabaa_syn = Synapse(id='GABAA', 
                          neuroml2_source_file='GABAA.synapse.nml')
    net.synapses.append(gabaa_syn)
                                

    
    net.projections.append(Projection(id='proj_mf_grc_ampa',
                                      presynaptic=pop_mf.id, 
                                      postsynaptic=pop_grc.id,
                                      synapse=mf_ampa_syn.id,
                                      delay=0,
                                      weight='weight_mf_grc_ampa',
                                      random_connectivity=RandomConnectivity(probability='0.33')))
                                      
    net.projections.append(Projection(id='proj_mf_grc_nmda',
                                      presynaptic=pop_mf.id, 
                                      postsynaptic=pop_grc.id,
                                      synapse=nmda_syn.id,
                                      delay=0,
                                      weight='weight_mf_grc_nmda',
                                      random_connectivity=RandomConnectivity(probability='0.33')))
                                      
    net.projections.append(Projection(id='proj_grc_gol_ampa',
                                      presynaptic=pop_grc.id, 
                                      postsynaptic=pop_gol.id,
                                      synapse=ampa_gr_gol_syn.id,
                                      delay=0,
                                      weight='weight_grc_gol',
                                      random_connectivity=RandomConnectivity(probability='.9')))
                                      
    net.projections.append(Projection(id='proj_gol_grc_ampa',
                                      presynaptic=pop_gol.id, 
                                      postsynaptic=pop_grc.id,
                                      synapse=gabaa_syn.id,
                                      delay=0,
                                      weight='weight_gol_grc',
                                      random_connectivity=RandomConnectivity(probability='0.33')))
    '''
    net.projections.append(Projection(id='projIinput',
                                      presynaptic=pIpoisson.id, 
                                      postsynaptic=pI.id,
                                      synapse='ampa',
                                      delay=delay_ext,
                                      weight=JE,
                                      one_to_one_connector=OneToOneConnector()))
                                      
           
    net.projections.append(Projection(id='projEE',
                                      presynaptic=pE.id, 
                                      postsynaptic=pE.id,
                                      synapse='ampa',
                                      delay='delay',
                                      weight=JE,
                                      random_connectivity=RandomConnectivity(probability='epsilon')))

    net.projections.append(Projection(id='projEI',
                                      presynaptic=pE.id, 
                                      postsynaptic=pI.id,
                                      synapse='ampa',
                                      delay='delay',
                                      weight=JE,
                                      random_connectivity=RandomConnectivity(probability='epsilon')))
    
    net.projections.append(Projection(id='projIE',
                                      presynaptic=pI.id, 
                                      postsynaptic=pE.id,
                                      synapse='gaba',
                                      delay='delay',
                                      weight=JI,
                                      random_connectivity=RandomConnectivity(probability='epsilon')))
                                      
    net.projections.append(Projection(id='projII',
                                      presynaptic=pI.id, 
                                      postsynaptic=pI.id,
                                      synapse='gaba',
                                      delay='delay',
                                      weight=JI,
                                      random_connectivity=RandomConnectivity(probability='epsilon')))'''

    #print(net)
    #print(net.to_json())
    new_file = net.to_json_file('%s.json'%net.id)


    ################################################################################
    ###   Build Simulation object & save as JSON

    sim = Simulation(id='Sim%s'%net.id,
                     network=new_file,
                     duration=simtime,
                     dt=dt,
                     seed= 123,
                     recordTraces={pop_grc.id:[0,1],pop_gol.id:'*'},
                     recordSpikes={pop_grc.id:'*',pop_gol.id:'*',pop_mf.id:'*'})

    sim.to_json_file()
    
    return sim, net



if __name__ == "__main__":

    if '-sweep' in sys.argv:
        
        sim, net = generate()
        sim.recordTraces={}
        
        fixed = {'dt':0.025, 'order':5}
 
        vary = {'eta':[0.5,1,1.5,2,3,4,5,6,7,8,9,10]}
        #vary = {'eta':[1,2,5]}
        #vary['seed'] = [i for i in range(10)]
        vary['seed'] = [i for i in range(5)]

        simulator = 'jNeuroML_NetPyNE'
        simulator = 'jNeuroML_NEURON'
        simulator = 'jNeuroML'
        simulator = 'PyNN_NEST'
        simulator = 'jNeuroML'

        nmllr = NeuroMLliteRunner('SimExample7.json',
                                  simulator=simulator)

        ps = ParameterSweep(nmllr, 
                            vary, 
                            fixed,
                            num_parallel_runs=4,
                            plot_all=False, 
                            heatmap_all=False,
                            show_plot_already=False,
                            peak_threshold=0)

        report = ps.run()
        ps.print_report()

        #  ps.plotLines('weightInput','average_last_1percent',save_figure_to='average_last_1percent.png')
        #ps.plotLines('weightInput','mean_spike_frequency',save_figure_to='mean_spike_frequency.png')
        #ps.plotLines('eta','Einput[0]/spike:mean_spike_frequency',save_figure_to='mean_spike_frequency.png')
        ps.plotLines('eta','expoisson/0/poisson_input/spike:mean_spike_frequency',second_param='seed',save_figure_to='mean_spike_frequency_ein.png')
        ps.plotLines('eta','inpoisson/0/poisson_input/spike:mean_spike_frequency',second_param='seed',save_figure_to='mean_spike_frequency_iin.png')
        ps.plotLines('eta','Epop/0/ifcell/spike:mean_spike_frequency',second_param='seed',save_figure_to='mean_spike_frequency_e.png')
        ps.plotLines('eta','Ipop/0/ifcell/spike:mean_spike_frequency',second_param='seed',save_figure_to='mean_spike_frequency_i.png')

        import matplotlib.pyplot as plt

        plt.show()
        
    if '-sweep2' in sys.argv:
        
        sim, net = generate()
        sim.recordTraces={}
        
        fixed = {'dt':0.025, 'order':5}
 
        vary = {'eta':[0.5,1,1.5,2,3]}
        vary = {'epsilon':[0.01,0.1,0.2,0.5,0.9]}
        vary = {'J':[0.01,0.1,0.2,0.5,0.9]}
        #vary = {'g':[0.5,1,1.5,2,3,20]}
        
        first = vary.keys()[0]
        
        #vary = {'eta':[1,2,5]}
        #vary['seed'] = [i for i in range(10)]
        vary['seed'] = [i for i in range(3)]

        simulator = 'jNeuroML'
        simulator = 'PyNN_NEST'
        simulator = 'jNeuroML_NetPyNE'
        simulator = 'jNeuroML'
        simulator = 'jNeuroML_NEURON'

        nmllr = NeuroMLliteRunner('SimExample7.json',
                                  simulator=simulator)

        ps = ParameterSweep(nmllr, 
                            vary, 
                            fixed,
                            num_parallel_runs=16,
                            plot_all=False, 
                            heatmap_all=False,
                            show_plot_already=False,
                            peak_threshold=0)

        report = ps.run()
        ps.print_report()

        #  ps.plotLines('weightInput','average_last_1percent',save_figure_to='average_last_1percent.png')
        #ps.plotLines('weightInput','mean_spike_frequency',save_figure_to='mean_spike_frequency.png')
        #ps.plotLines('eta','Einput[0]/spike:mean_spike_frequency',save_figure_to='mean_spike_frequency.png')
        
        second = 'seed'
        ps.plotLines(first,'expoisson/0/poisson_input/spike:mean_spike_frequency',second_param=second,save_figure_to='mean_spike_frequency_ein.png')
        ps.plotLines(first,'inpoisson/0/poisson_input/spike:mean_spike_frequency',second_param=second,save_figure_to='mean_spike_frequency_iin.png')
        ps.plotLines(first,'Epop/0/ifcell/spike:mean_spike_frequency',second_param=second,save_figure_to='mean_spike_frequency_e.png')
        ps.plotLines(first,'Ipop/0/ifcell/spike:mean_spike_frequency',second_param=second,save_figure_to='mean_spike_frequency_i.png')

        import matplotlib.pyplot as plt

        plt.show()
    
    else:

        sim, net = generate()

        ################################################################################
        ###   Run in some simulators

        import sys

        check_to_generate_or_run(sys.argv, sim)

