edit_btn = document.querySelector('.model-btn')
modal = document.querySelector('.modal-bg')
modal_close = document.querySelector('.modal-close')

edit_btn.addEventListener('click', function(){
    modal.classList.add('model-active')
})
modal_close.addEventListener('click', function(){
    console.log('closing....')
    modal.classList.remove('model-active')
})