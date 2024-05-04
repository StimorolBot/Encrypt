export const createUrlDownload = ( data, name ) => {
    let url = URL.createObjectURL( data );
            let anchor = document.createElement("a");
            
            anchor.href = url;
            anchor.download = name;
            document.body.append(anchor);
            anchor.style = "display: none";
            anchor.click();
            anchor.remove();
}

