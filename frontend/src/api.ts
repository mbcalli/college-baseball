import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface PlayerStatistic {
  name: string;
  value: number;
  percentile: number;
  formatted_value: string;
}

export interface PlayerProfile {
  id: string;
  name: string;
  team: string;
  statistics: PlayerStatistic[];
  stat_type: string;
  is_advanced: boolean;
}

export interface TeamRoster {
  team: string;
  batters: string[];
  pitchers: string[];
}

export interface DataDateInfo {
  year: number;
  last_update: string;
}

export interface DataDatesResponse {
  years: DataDateInfo[];
}

export const getTeams = async (year?: number): Promise<string[]> => {
  const response = await api.get('/api/teams', {
    params: year ? { year } : {},
  });
  return response.data;
};

export const getYears = async (): Promise<number[]> => {
  const response = await api.get('/api/years');
  return response.data;
};

export const getDataDates = async (): Promise<DataDatesResponse> => {
  const response = await api.get('/api/data-dates');
  return response.data;
};

export const getTeamRoster = async (team: string, year?: number): Promise<TeamRoster> => {
  const response = await api.get(`/api/teams/${team}/roster`, {
    params: year ? { year } : {},
  });
  return response.data;
};

export const getPlayerBatting = async (
  playerName: string,
  advanced: boolean = true,
  year?: number
): Promise<PlayerProfile> => {
  const response = await api.get(`/api/players/${playerName}/batting`, {
    params: { 
      advanced,
      ...(year ? { year } : {}),
    },
  });
  return response.data;
};

export const getPlayerPitching = async (
  playerName: string,
  advanced: boolean = true,
  year?: number
): Promise<PlayerProfile> => {
  const response = await api.get(`/api/players/${playerName}/pitching`, {
    params: { 
      advanced,
      ...(year ? { year } : {}),
    },
  });
  return response.data;
};

export default api;
