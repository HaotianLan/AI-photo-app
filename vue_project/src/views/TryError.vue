<template>
    <div>
      <input v-model="searchQuery" @input="fetchRecommendations" placeholder="Search..." />
      <div v-if="recommendedImages.length">
        <div v-for="imageUrl in recommendedImages" :key="imageUrl">
          <img :src="imageUrl" alt="Recommended Image" />
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        searchQuery: '',
        recommendedImages: []
      };
    },
    methods: {
      async fetchRecommendations() {
        const params = {
            q: '人数',
            selectedTags: '国风'
        }
        try {
          const response = await axios.post(
            'http://localhost:5001/recommend', 
            params
          );
          console.log('Full response:', response);
          this.recommendedImages = response.data.recommended_images;
        } catch (error) {
          console.error('Error fetching recommendations:', error);
          alert('Failed to fetch recommendations. Please try again.');
        }
      }
    }
  };
  </script>