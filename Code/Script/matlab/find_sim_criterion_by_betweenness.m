function results=find_sim_criterion_by_betweenness()
    global adj_content_full
    
    load adj_content_full
    
    one_component_criterion=0.53715717792510986328125;
    
    %edge_sims=unique(adj_content_full(adj_content_full<one_component_criterion));
    edge_sims=0.3:0.01:0.53;
    total=length(edge_sims);
    results=zeros(total,2);

    for x=1:1:total
        sprintf('%f:%d',x,total)
        [EBC,BC]=edge_betweenness_bin(adj_content_full>edge_sims(x));
        results(x,1)=edge_sims(x);
        results(x,2)=find_max_bet_div_sim(EBC);
    end
end

function max_bet_div_sim=find_max_bet_div_sim(EBC)
% input EBC: edge betweenness matrix
    global adj_content_full
    
    max_bet=max(max(EBC));
    [r,c]=find(EBC==max_bet);
    count=length(r);
    max_bet_div_sim=-1;
    for x=1:1:count
        sim=adj_content_full(r(x),c(x));
        max_bet_div_sim=max(max_bet_div_sim,max_bet/sim);
    end
end