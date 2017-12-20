var home = new Vue({
    el: '#photos',
    delimiters: ['[[', ']]'],
    data: {
        urls: {
            'photo': window.location.origin +'/api/v1/photos/',
        },
        cookie: _get_cookie('csrftoken'),
        photos: [],
        filter_text: "",
        next_url: '',
        modal_photo: {},
        modal_photo_index: 0,
        selected_indices: [],
        multiselect_mode: false,
        bulk_tag: '',
    },
    computed: {
        show_prev: function(){
            return (this.page > 0 ? true : false)
        },
        show_next: function(){
            return (this.page_size * (this.page + 1) < this.photos.length ? true : false)
        },
        display_page: function(){
            return this.page + 1;
        },
        download_filename: function(){
            let url = this.modal_photo.image;
            return (url ? url.slice(url.lastIndexOf('/')+1) : '');
        },
        disable_buttons: function(){
            return (this.selected_indices.length > 0 ? false : true)
        },
        selected_ids: function(){
            return this.selected_indices.map(photo_index => this.photos[photo_index].id)
        },
        selected_photos: function(){
            return this.selected_indices.map(
                photo_index => new Photo(this.photos[photo_index]) 
            )
        }
    },
    methods: {
        load_next_page: function(){
            if(this.next_url){this.get_next_photo()}
        },
        next_photo: function(){
            this.modal_photo_index += 1;
            this.modal_photo = this.photos[this.modal_photo_index];
        },
        prev_photo: function(){
            this.modal_photo_index -= 1;
            this.modal_photo = this.photos[this.modal_photo_index];
        },
        get_photos: function(query){
            Photo.search(query).then( data => {
                this.photos = data.data.results;
                this.next_url = data.data.next;
            })
        },
        get_next_photo: function(){
            if(this.next_url){
                axios.get(this.next_url).then( data => {
                    this.photos = this.photos.concat(data.data.results);
                    this.next_url = data.data.next;
                })
            }
        },
        set_modal_photo: function(photo, index){
            this.modal_photo = photo;
            this.modal_photo_index = index;
        },
        get_untagged: function(){
            this.filter_text = 'untagged';
        },
        clear_filter: function(){
            this.filter_text = '';
        },
        toggle_multiselect: function(){
            this.multiselect_mode = !this.multiselect_mode;
            this.selected_indices = [];
        },
        select_photo: function(index){
            if(this.selected_indices.includes(index)){
                this.selected_indices.splice(
                    this.selected_indices.indexOf(index),
                    1
                );
            }else{
                this.selected_indices.push(index);
            }
        },
        is_selected: function(index){
            return this.selected_indices.includes(index);
        },
        delete_selected: function(){
            let promises = Photo.delete_photos(this.selected_photos)
            axios.all(promises)
            .then( response => {
                this.get_photos(this.filter_text);
                this.selected_indices = []
            })
            .catch( error => {
                console.log(error)
            })
        },
        tag_selected: function(){
            Tag.create_tag(this.bulk_tag);
            
            let photos = this.selected_photos.slice();
            photos.forEach(photo => photo.tags.push(this.bulk_tag))
            let promises = Photo.update_photos(photos);

            axios.all(promises)
            .then( response => {
                this.bulk_tag = '';
            })
            .catch( error => {
                console.log(error)
            })
        },
        delete_modal_photo: function(){
            let promise = Photo.delete_photo(new Photo(this.modal_photo));
            promise.then( response => {
                this.get_photos(this.filter_text);
            }).catch( error => console.log(error))
        },
    },
    watch:{
        filter_text: function(query){
            this.get_photos(query);
            this.multiselect_mode = false;
        }
    },
    mounted: function(){
        this.get_photos('');
        window.onscroll = (ev) => {
            console.log('a')
            if ((window.innerHeight + window.scrollY) == document.body.offsetHeight){
                console.log('b')
                this.load_next_page()
            }
        };
    }
})
