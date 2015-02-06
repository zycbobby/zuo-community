function cause_less_component_edge_sim=find_one_component_clique(adj_content_full)
    load adj_content_full
    adj_content_full_sparse=sparse(adj_content_full);
    lower_bound=0.01;
    upper_bound=0.9;
    
    while 1
        mid=(lower_bound+upper_bound)/2;
        [l_c,m_c,cause_less_component_edge_sim]=get_components_by_similarity(adj_content_full_sparse,mid);
        sprintf('mid:%f, l_c:%d, m_c:%d',mid,l_c,m_c)
        if l_c==1 && m_c>1
            break
        else
            if l_c>1
                upper_bound=mid;
            end
            if m_c==1
                lower_bound=mid;
            end
        end
    end
    
end

function [l_c,m_c,cause_less_component_edge_sim]=get_components_by_similarity(adj_sparse, similarity)
    % find the min sim over similarity
    t_array_sparse=min(min(adj_sparse(find(adj_sparse.*(adj_sparse>similarity)))));
    cause_more_component_edge_sim=t_array_sparse(1,1);
    % find the max sim below similarity\
    t_array_sparse=max(max(adj_sparse.*(adj_sparse<similarity)));
    cause_less_component_edge_sim=t_array_sparse(1,1);
    
    [l_c,c1]=graphconncomp(adj_sparse>cause_less_component_edge_sim,'Directed',false);
    [m_c,c2]=graphconncomp(adj_sparse>cause_more_component_edge_sim,'Directed',false); 
end