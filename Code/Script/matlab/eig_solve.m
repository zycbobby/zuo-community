function eig_solve()
% this function aim to compute the largest algerabic eigenvector of the
% given matrix
% moreover I have to write the result to the file system
load adj

adj=double(adj);

[rows cols]=size(adj);

% define the queue
global q q_head q_tail;

q=zeros(1,10000);
q_head=1;
q_tail=1;

% next_label going to use
next_label=2;

% first init all the label 
com_list=ones(1,rows);
pushq(1);

% this modularity matrix should be persistant because it is used to compute
% the whole modularity
B=compute_modularity_matrix_easy(adj);

%compute old modularity
old_modularity=compute_modularity(B,com_list,adj);


while q_head~=q_tail
    % compute the eigenvector
    com=getq();
    % find the index of the nodes that belong to the given community
    indexes_needed=find(com_list==com);
    
    %sub adj matrix by the indexes
    sub_adj=adj(indexes_needed,indexes_needed);
    
    %compute the corresponding modularity matrix
    sub_mod=compute_modularity_matrix_easy(sub_adj);
    
    [la_vector,la_value]=eigs(sub_mod,1,'la');    
    p_index=find(la_vector>0);
    n_index=find(la_vector<=0);
    positive_count=length(p_index);
    negative_count=length(n_index);
    
    if positive_count==0 || negative_count==0
        continue
    end
    
    t_membership=com_list;
    % assign new label
    for x=1:1:negative_count
        t_membership(1,indexes_needed(n_index(x)))=next_label;
    end

    new_modularity=compute_modularity(B,t_membership,adj);
    
    if new_modularity>old_modularity
        old_modularity=new_modularity;
        com_list=t_membership;
        pushq(com);
        pushq(next_label);
        next_label=next_label+1;
    end
end

fid=fopen('community.list','w');
for x=1:1:length(com_list)
    fprintf(fid, '%d ',com_list(x));
end
fclose(fid);

end

function Q=compute_modularity(B, com_list,adj)
    H=get_indicator_matrix(adj,com_list);
    [rows cols]=size(H);
    totalQ=0.0;
    for com=1:1:cols
        totalQ=totalQ+H(:,com)'*B*H(:,com);
    end
    Q=totalQ/sum(sum(adj));
end

function com_label=getq()
global q q_head
    % get an element from a queue
    com_label=q(1,q_head);
    q_head=q_head+1;
end

function pushq(com_label)
global q q_tail
    q(1,q_tail)=com_label;
    q_tail=q_tail+1;
end




function mod_matrix=compute_modularity_matrix(adj)
% first compute modularity matrix
edge_count=sum(sum(adj));
[rows cols]=size(adj);
mod_matrix=zeros(rows, cols, 'double');
for r=1:1:rows
    rdegree=sum(adj(r,:));
    for c=r:1:cols
        cdegree=sum(adj(:,c));
        temp=double(adj(r,c))-(rdegree*cdegree/edge_count);
        mod_matrix(r,c)=temp;
        mod_matrix(c,r)=temp;
    end
end
end


function B=compute_modularity_matrix_easy(adj)
% first compute modularity matrix
K=sum(adj);
edge_count=sum(K);
B=double(adj)-(K.'*K)/edge_count;
end

function H = get_indicator_matrix(adj,com)

% Create the indicator matrix from a community list
% giving for each node its community.
%
% Input
%   - adj: symmetrical (binary or weighted) adjacency matrix
%   - com: community list
%
% Output
%   - H: community indicator matrix where H(i,j) is 1 if node i belongs to
%        community j
%
% Author: Erwan Le Martelot
% Date: 06/12/10

    % Number of nodes
    n = length(com);

    % Number of communities
    nc = length(unique(com));

    % Initialise indicator matrix
    H = zeros(n,nc);

    % Fill in matrix
    for i=1:n
        H(i,com(i)) = 1;
    end

end