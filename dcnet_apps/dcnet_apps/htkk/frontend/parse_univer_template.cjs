const XLSX = require('xlsx');
const fs = require('fs');

const file = '/home/long/frappe-bench-v16/apps/dcnet_apps/dcnet_apps/htkk/docs/htkk_InterfaceTemplates/Excel/01_GTGT_TT80_283.xls';
if (!fs.existsSync(file)) {
  console.log("File not found");
  process.exit(1);
}

const wb = XLSX.readFile(file, {cellStyles: true});
const ws = wb.Sheets[wb.SheetNames[0]];
const range = XLSX.utils.decode_range(ws['!ref']);

const univerData = {
  id: 'workbook-1',
  name: '01_GTGT',
  sheets: {
    'sheet-01': {
      id: 'sheet-01',
      name: '01/GTGT',
      cellData: {},
      columnData: {},
      rowData: {},
      mergeData: [],
      columnCount: range.e.c + 5,  // actual cols + margin
      rowCount: range.e.r + 10     // actual rows + margin
    }
  }
};

const sheet = univerData.sheets['sheet-01'];

for(let R = 0; R <= range.e.r; ++R) {
  sheet.rowData[R] = { h: 25 }; 
  for(let C = 0; C <= range.e.c; ++C) {
    if(!sheet.columnData[C]) sheet.columnData[C] = { w: 100 };
    
    const cell_address = {c:C, r:R};
    const cell_ref = XLSX.utils.encode_cell(cell_address);
    const cell = ws[cell_ref];
    if(!cell) continue;
    
    if(!sheet.cellData[R]) sheet.cellData[R] = {};
    
    let t = 1;
    if (cell.t === 'n') t = 2; // number
    
    let v = cell.v !== undefined ? cell.v : '';
    
    // basic styling
    let s = {};
    if (cell.s) {
       if (cell.s.font && cell.s.font.bold) s.bl = 1;
       if (cell.s.font && cell.s.font.sz) s.fs = cell.s.font.sz;
       if (cell.s.alignment && cell.s.alignment.horizontal) {
          if (cell.s.alignment.horizontal === 'center') s.ht = 2;
          else if (cell.s.alignment.horizontal === 'right') s.ht = 3;
       }
    }
    
    sheet.cellData[R][C] = { v, t, s };
  }
}

if (ws['!merges']) {
  ws['!merges'].forEach(merge => {
    sheet.mergeData.push({
      startRow: merge.s.r,
      endRow: merge.e.r,
      startColumn: merge.s.c,
      endColumn: merge.e.c
    });
  });
}

if (ws['!cols']) {
  ws['!cols'].forEach((col, idx) => {
    if (col && col.wpx) sheet.columnData[idx] = { w: col.wpx };
    else if (col && col.wch) sheet.columnData[idx] = { w: col.wch * 8 };
  });
}
if (ws['!rows']) {
  ws['!rows'].forEach((row, idx) => {
    if (row && row.hpx) sheet.rowData[idx] = { h: row.hpx };
    else if (row && row.hpt) sheet.rowData[idx] = { h: row.hpt * 1.33 };
  });
}

fs.writeFileSync('template.json', JSON.stringify(univerData, null, 2));
console.log('Generated template.json');
