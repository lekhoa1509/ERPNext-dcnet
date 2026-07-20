const XLSX = require('xlsx');
const wb = XLSX.readFile('./public/test_sample.xls');
const ws = wb.Sheets[wb.SheetNames[0]];

const cellData = {};
const range = XLSX.utils.decode_range(ws['!ref']);

for(let R = range.s.r; R <= range.e.r; ++R) {
  for(let C = range.s.c; C <= range.e.c; ++C) {
    const cell_address = {c:C, r:R};
    const cell_ref = XLSX.utils.encode_cell(cell_address);
    const cell = ws[cell_ref];
    if(!cell) continue;
    
    if(!cellData[R]) cellData[R] = {};
    
    // t: cell type (s: string, n: number)
    let type = 1; // default string in Univer
    if (cell.t === 'n') type = 2; // number
    
    cellData[R][C] = {
      v: cell.v,
      t: type
    };
  }
}
console.log("Rows parsed: " + Object.keys(cellData).length);
