detail = new Vue({
    el: '#detail',
    delimiters: ['[[', ']]'],
    data: {
        urls: {
            'photo': window.location.origin +'/api/v1/photos/',
            'tags': window.location.origin +'/api/v1/tags/'
        },
        cookie: _get_cookie('csrftoken'),
        photo: '',
        photo_url: '',
        year: '',
        month: '',
        day: '',
        tags: [],
        uploaded: [],
        new_tag: '',
        success_text: '',
        error_text: '',
    },
    methods: {
        loadData: function(data){
            console.log(data)
            this.year = data.year;
            this.month = data.month;
            this.day = data.day;
            this.tags = data.tags;
            this.photo_url = data.image;
            this.photo = data;
        },
        removeTag: function(tag){
            this.tags = this.tags.filter(el => el !== tag);
        },
        addTag: function(){
            this.tags.push(this.new_tag)
            this.new_tag = '';
        },
        submit: function(){
            this.success_text = '';
            this.error_text = '';
            if(this.tags.length > 0){
                this.uploadTags();
            }else{
                this.update_photo();
            }
        },
        uploadTags: function(){
            let promises = Tag.create_tags(this.tags)
            axios.all(promises)
            .then(this.update_photo())
            .catch(this.update_photo())
        },
        update_photo: function(){
            let photo = new Photo(this.photo);
            Object.assign(photo, this.photo)
            Photo.update_photo(photo)
            .then( response => {
                this.success_text = "Update successful!";
            })
            .catch( error => {
                this.error_text = error;
            })
        },
        delete_photo: function(){
            let photo = new Photo(this.photo);
            Photo.delete_photo(photo)
            .then( response => {
                this.success_text = "Delete successful!"
                document.location.href = "/";
            })
            .catch( error => this.error_text = error)
        }
    },
    mounted: function(){
        axios.get(this.urls.photo + photo_id)
        .then( response => this.loadData(response.data) )
        .catch( error => console.log(error) );
    }
})