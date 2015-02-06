load evaluation_data
[sim,k,l]=size(data);
sim_keys=[0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95];
sim_length=length(sim_keys);
k_keys=[4,5,6,7,8,9,10];
k_length=length(k_keys);
l_keys=[4,6,8,10,12,14,16];
l_length=length(l_keys);

grid on
hold on
for sim_index=1:1:sim_length
    title_name=strcat('sim_criterion=',num2str(sim_keys(sim_index)));
    l_index=1;
    subplot(3,6,sim_index),plot(k_keys,reshape(data(sim_index,:,l_index),1,length(data(sim_index,:,l_index))),'y-'),axis([min(k_keys),max(k_keys),0,0.3]),title(title_name),hold on,grid on
    l_index=2;
    subplot(3,6,sim_index),plot(k_keys,reshape(data(sim_index,:,l_index),1,length(data(sim_index,:,l_index))),'r-'),axis([min(k_keys),max(k_keys),0,0.3]),title(title_name),hold on,grid on
    l_index=3;
    subplot(3,6,sim_index),plot(k_keys,reshape(data(sim_index,:,l_index),1,length(data(sim_index,:,l_index))),'g-'),axis([min(k_keys),max(k_keys),0,0.3]),title(title_name),hold on,grid on
    l_index=4;
    subplot(3,6,sim_index),plot(k_keys,reshape(data(sim_index,:,l_index),1,length(data(sim_index,:,l_index))),'b-'),axis([min(k_keys),max(k_keys),0,0.3]),title(title_name),hold on,grid on
    l_index=5;
    subplot(3,6,sim_index),plot(k_keys,reshape(data(sim_index,:,l_index),1,length(data(sim_index,:,l_index))),'c-'),axis([min(k_keys),max(k_keys),0,0.3]),title(title_name),hold on,grid on
    l_index=6;
    subplot(3,6,sim_index),plot(k_keys,reshape(data(sim_index,:,l_index),1,length(data(sim_index,:,l_index))),'m-'),axis([min(k_keys),max(k_keys),0,0.3]),title(title_name),hold on,grid on
    l_index=7;
    subplot(3,6,sim_index),plot(k_keys,reshape(data(sim_index,:,l_index),1,length(data(sim_index,:,l_index))),'k-'),axis([min(k_keys),max(k_keys),0,0.3]),title(title_name),hold on,grid on
end





% for l_index=1:1:l_length
%     sim_vector=zeros(1,k_length);
%     sim_vector=sim_vector+0.1;
%     plot3(sim_vector,k_keys,data(1,:,l_index),'r');
%     grid on
%     hold on
% end
