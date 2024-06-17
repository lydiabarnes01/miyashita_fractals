function select_images(varargin)

p = inputParser;
addOptional(p,'im_path','./img',@(x) ischar(x));
parse(p,varargin{:});
im_path = p.Results.im_path;

in = dir(fullfile(im_path,'*.png'));

for i = 1:size(in,1)
    fnl = fullfile(im_path,in(i).name);

    im = imread(fnl);
    imshow(im); title(fnl);

    keys = input("reject? (0 = keep, 1 = discard): ",'s'); 
    reject = str2double(keys);

    to_fnl = fullfile(im_path,'discard',in(i).name);
    if reject == 1
        movefile(fnl,to_fnl);
    end


end

end