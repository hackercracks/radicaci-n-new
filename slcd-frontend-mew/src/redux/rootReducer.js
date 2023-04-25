import authSliceReducer from "./features/authSlice";
import fileSlice from "./features/fileSlice";
import trackSlice from "./features/trackSlice";

const rootReducer = {
  track: trackSlice,
  auth: authSliceReducer,
  files: fileSlice,
};

export default rootReducer;
