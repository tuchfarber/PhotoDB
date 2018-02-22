upload_form = new Vue({
    el: '#upload_form',
    delimiters: ['[[', ']]'],
    data: {
        urls: {
            'photo': window.location.origin +'/api/v1/photos/',
        },
        cookie: _get_cookie('csrftoken'),
        photos: [],
        uploaded: [],
        year: '',
        month: '',
        day: '',
        tags: [],
        new_tag: '',
        errors: [],
        upload_index: 0
    },
    methods: {
        reset: function(){
            this.uploaded = [];
            this.errors = [];
            this.upload_index = 0;
        },
        removeTag: function(tag){
            this.tags = this.tags.filter(el => el !== tag);
        },
        addTag: function(){
            this.tags.push(this.new_tag)
            this.new_tag = '';
        },
        processPhotos: function(event){
            this.photos = event.target.files
        },
        submit: function(){
            this.reset()
            if(this.tags.length > 0){
                let promises = Tag.create_tags(this.tags);
                axios.all(promises)
                .then( response => {
                    this.uploadPhoto();
                })
                .catch( error => {
                    this.uploadPhoto();
                })
            }else{
                this.uploadPhoto();
            }
        },
        tagError: function(error){
            console.log(error)
        },
        uploadPhoto: function(){
            photo = this.photos[this.upload_index]
            data = new FormData();
            data.append('image', photo);
            data.append('year', this.year);
            data.append('month', this.month);
            data.append('day', this.day);
            this.tags.forEach(function(tag){
                data.append('tags', tag)
            })
            axios({
                method: 'post',
                url: this.urls['photo'],
                data: data,
                headers: {
                    'X-CSRFToken': this.cookie
                }
            })
            .then( response => {
                this.uploaded.push(response.data);
                this.upload_index += 1
                if(this.upload_index < this.photos.length){
                    this.uploadPhoto()
                }
            })
            .catch( error => {
                let msg = error.response.data[0]
                console.log(msg)
                this.errors.push(msg)
                this.upload_index += 1
                if(this.upload_index < this.photos.length){
                    this.uploadPhoto()
                }
            })
        }
    }
})