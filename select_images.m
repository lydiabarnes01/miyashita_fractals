function select_images(varargin)

p = inputParser;
addOptional(p,'im_path','./img',@(x) ischar(x));
parse(p,varargin{:});
im_path = p.Results.im_path;

in = dir(fullfile(im_path,'*square.png'));

%% remove colour
% for i = 1:size(in,1)
%     fnl = fullfile(im_path,in(i).name);
%     [im,~,alpha] = imread(fnl);
%     idx = im(:,:,2)~=0;
%     im = uint8(repmat(idx*255,1,1,3));
%     imwrite(im,fnl,'Alpha',alpha);
% end

%% select
% figure;
% for i = 1:size(in,1)
%     fnl = fullfile(im_path,in(i).name);
% 
%     im = imread(fnl);
%     imshow(im); title(fnl);
% 
%     keys = input("reject? (0 = keep, 1 = discard): ",'s'); 
%     reject = str2double(keys);
% 
%     to_fnl = fullfile(im_path,'discard',in(i).name);
%     if reject == 1
%         movefile(fnl,to_fnl);
%     end
% 
% end

%% add colour
rng(12345);
colour_names = {'green','teal','blue'}; 
colour_degrees = [160,180,200];

x = 1:360;
y = rescale(x)';
hsl = [y ones(size(y,1),1) repmat(.4,size(y,1),1)];
rgb = round(hsl2rgb(hsl)*255);

s = 10;
m = 0;
l = -12;
u = 12;
for i = 1:size(in,1)
    dnorm(i,1) = round(m+s*trandn((l-m)/s,(u-m)/s));
end

for i = 1:size(in,1)
    fnl = fullfile(im_path,in(i).name);
    [im,~,alpha] = imread(fnl);
    idx = im(:,:,1) == 255;

    for ii = 1:size(colour_names,2)

        this_rgb = rgb(colour_degrees(ii)+dnorm(i),:);        
        for j = 1:size(this_rgb,2)
            im(:,:,j) = idx*this_rgb(j);
        end

        [~,name,ext] = fileparts(in(i).name);
        fnl = fullfile(im_path,[name '-' colour_names{ii} ext]);
        imwrite(im,fnl,'Alpha',alpha);
    end
end

end