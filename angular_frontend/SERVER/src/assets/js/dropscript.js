async function delay(ms) {
    return new Promise( resolve => setTimeout(resolve, ms) );
}

try{
    const mouseOver = (()=>{
        const dropdowns = document.querySelectorAll('.dropdown');
        const dropups = document.querySelectorAll('.dropup');
        dropdowns.forEach(dropdown => {
            dropdown.addEventListener('mouseover', function hoverOn(event) {
                try{dropdown.children[1].classList.add('show');}
                catch{}
            });
            dropdown.addEventListener('mouseout', async function hoverOut(event) {
                try{dropdown.children[1].classList.remove('show');}
                catch{}
            });
        });
        
        dropups.forEach(dropup => {
            dropup.addEventListener('mouseover', function hoverOn(event) {
                dropup.children[1].classList.add('show');
            });
            dropup.addEventListener('mouseout', async function hoverOut(event) {
                
                dropup.children[1].classList.remove('show');
            });
        });
    }) 
    mouseOver()
}
catch(err){}
