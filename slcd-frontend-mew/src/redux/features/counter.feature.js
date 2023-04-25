import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  count: 0,
};

let counterSlice = createSlice({
  name: "counter",
  initialState: initialState,
  reducers: {
    increament: function (state, action) {
      state.count = state.count + 1;
    },
    increamentBy: function (state, action) {
      state.count = state.count + action.payload;
    },
    decreament: function (state, action) {
      state.count = state.count - 1;
    },
  },
});

export const { increament, increamentBy, decreament } = counterSlice.actions;
export default counterSlice.reducer;
