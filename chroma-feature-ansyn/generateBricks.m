mat = gamePort('StartGamePlay.wav');
rows=zeros(4, 28);
for i=1:56
m = mat(:,((i-1)*50+1):i*50);

value = max(max(m));
[row, col] = find(value==m);
rows(1, i) = row;
m(row, col) = -100;

value = max(max(m));
[row, col] = find(value==m);
rows(2, i) = row;
m(row, col) = -100;

value = max(max(m));
[row, col] = find(value==m);
rows(3, i) = row;
m(row, col) = -100;

value = max(max(m));
[row, col] = find(value==m);
rows(4, i) = row;
m(row, col) = -100;

end