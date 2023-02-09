function html2pdf(filename='default', filename2='default'){
    document.querySelector('.export_pdf_btn').addEventListener("click", () => {
        const invoice = document.getElementById("table_data");
    
                var opt = {
                    margin: 1,
                    filename:  filename+'.pdf',
                    image: { type: 'jpeg', quality: 0.98 },
                    html2canvas: { scale: 2 },
                    jsPDF: { unit: 'in', format: 'letter', orientation: 'landscape'}
                };
                html2pdf().from(invoice).set(opt).save();
     })
    
    
    //  document.querySelector('.export_pdf_btn2').addEventListener("click", () => {
    //     const invoice = document.getElementById("table_data2");
    
    //             var opt = {
    //                 margin: 1,
    //                 filename: filename2+'.pdf',
    //                 image: { type: 'jpeg', quality: 0.98 },
    //                 html2canvas: { scale: 2 },
    //                 jsPDF: { unit: 'in', format: 'letter', orientation: 'landscape'}
    //             };
    //             html2pdf().from(invoice).set(opt).save();
    //  })
}