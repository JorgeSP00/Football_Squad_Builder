import axios from 'axios';


const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000',  // URL of the API
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getPlayers = async () => {
  try {
    const response = await apiClient.get('/players/');
    return response.data;
  } catch (error) {
    console.error('Error fetching data:', error);
    throw error;
  }
};

export const getNationalities = async () => {
  try {
    const response = await apiClient.get('/nationalities/');
    return response.data;
  } catch (error) {
    console.error('Error fetching nationalities:', error);
    throw error;
  }
};

export const getTeams = async () => {
  try {
    const response = await apiClient.get('/teams/');
    return response.data;
  } catch (error) {
    console.error('Error fetching teams:', error);
    throw error;
  }
};

export const getCompetitions = async () => {
  try {
    const response = await apiClient.get('/competitions/');
    return response.data;
  } catch (error) {
    console.error('Error fetching competitions:', error);
    throw error;
  }
};

export const getFilteredPlayers = async (competition_id = null, nationality_id = null, market_value = null) => {
  try {
    const params = {};

    if (competition_id !== null && competition_id !== "") {
      params.competition_id = competition_id;
    }

    if (nationality_id !== null && nationality_id !== "") {
      params.nationality_id = nationality_id;
    }

    if (market_value !== null && market_value !== "") {
      params.market_value = market_value;
    }

    const response = await apiClient.get('/players_filtered/', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching filtered players:', error);
    throw error;
  }
};

export const postSquad = async (competition_id = null, nationality_id = null, budget = null, user_id, squad_name = null) => {
  try {
      if (!competition_id) {
        competition_id=null;
      }
      if (!nationality_id) {
        nationality_id=null;
      }
      if (!budget) {
        budget=1000000000;
      }
      if(!squad_name) {
        squad_name = "New Squad"
      }
      const dataSquad = {
        name: squad_name,
        formation_id: 1,
        user_id: user_id,
        competition_id: competition_id,
        nationality_id: nationality_id,
        budget: budget,
      };

      const response = await apiClient.post('/squads/', dataSquad);
      return response;
  } catch (error) {
    console.error('Error posting squad:', error);
    throw error;
  }
};

export const postSquadPlayers = async (players = [], squad_id) => {
  try {
    const savedPlayers = []
    for (const player of players) {
      const dataPlayer = {
        squad_id: squad_id,
        player_id: player.player_id,
        position: player.position,
      };

      savedPlayers.push(await apiClient.post('/squad_players/', dataPlayer));
      
    }
    return savedPlayers;
  } catch (error) {
    console.error('Error posting squad players:', error);
    throw error;
  }
}

export const putSquadPlayers = async (players = [], squad_id) => {
  try {
    for (const player of players) {
      const dataPlayer = {
        squad_id: squad_id,
        player_id: player.player_id,
        position: player.position,
      };

      await apiClient.put('/squad_players/' + player.id, dataPlayer);
      
    }
  } catch (error) {
    console.error('Error putting squad players:', error);
    throw error;
  }
  
}

export const deleteSquadPlayers = async (players = []) => {
    try {
      for (const player of players) {
        await apiClient.delete('/squad_players/' + player);
      }
    } catch (error) {
      console.error('Error deleting squad players:', error);
      throw error;
    }
    
  }

  export const getUserSquads = async (user_id) => {
    try {
      const params = {};
      params.user_id = parseInt(user_id);

      const response = await apiClient.get('/squads_filtered/', {params});
      return response.data;
    } catch (error) {
      console.error('Error fetching competitions:', error);
      throw error;
    }
  };

  export const verifyUser = async (username = null, password = null) => {
    const params = {};

    params.username = username;
    params.password = password;
    const response = await apiClient.post('/users/verify/', params);
    return response.data;
  };



export const getSquadPlayers = async (squad_id = null) => {
  try {
    const response = await apiClient.get('/players_in_squad/' + parseInt(squad_id));
    return response.data;
  } catch (error) {
    console.error('Error fetching filtered players:', error);
    throw error;
  }
};

export const postNewUser = async (username, email, password) => {
  try {
    const params = {};
    params.username = username;
    params.email = email;
    params.password = password;
    await apiClient.post('/users/', params)
  } catch (error) {
    console.error('Error creating new user:', error);
    throw error;
  }
}