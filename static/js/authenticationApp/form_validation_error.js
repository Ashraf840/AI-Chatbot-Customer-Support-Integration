var error_div = document.querySelector("#errorDiv");

if (error_div != null) {
    var close_btn = document.querySelector("#outer");
    var flash_msg_close_label = document.querySelector("#flash_msg_close_label");
    close_btn.addEventListener("mouseover", (e) => {
        // console.log(`Mouse is hovered inside!`);
        flash_msg_close_label.style.opacity = 1;
    });
    
    close_btn.addEventListener("mouseout", (e) => {
        // console.log(`Mouse is hovered out!`);
        flash_msg_close_label.style.opacity = 0;
    });
    
    close_btn.addEventListener("click", (e) => {
        error_div.remove();
    });
}