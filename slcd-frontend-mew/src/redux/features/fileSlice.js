import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import API from "../api";

const initialState = {
  fileById: null,
  verifyy: null,
  file_num: null,
  files: null,
  unassigned_files: null,
  user: null,
  users: null,
  profile_id: null,
  error: "",
  loading: false,
};

export const getFiles = createAsyncThunk("files/fetch", async () => {
  let response = await API.get("files");
  // console.log(response.data)
  return response.data;

});

export const getAgent = createAsyncThunk("agent/fetch", async () => {
  let response = await API.get("assign-retrieve/");
  console.log("All Agent List",response.data)
  return response.data;
});

export const getFilesById = createAsyncThunk(
  "api/files/id",
  async (id, { rejectWithValue }) => {
    try {
      // console.log("test", id)
      const res = await API.get(`files/${id}`);
      // console.log(res.data);
      return res.data;
    } catch (err) {
      console.log("11", err);
      return rejectWithValue(err.response.data);
    }
  }
);

export const deleteFilesById = createAsyncThunk(
  "api/files/delete/id",
  async ({ id, router, toast }, { rejectWithValue }) => {
    try {
      // console.log("test", id)
      const res = await API.delete(`files/${id}`);
      toast.success("Deleted Successfully");
      console.log(res.data);
      // return res.data;
      setTimeout(() => {
        router.push("/files");
      }, 3000);
      // router.push("/files");
    } catch (err) {
      console.log("delete File", err);
      return rejectWithValue(err.response.data);
    }
  }
);

export const fileCreateStore = createAsyncThunk(
  "file/createzzz/",
  async ({ formData, toast, router }, { rejectWithValue }) => {
    try {
      const response = await API.post("files", formData);
      toast.success("Created Successfully");
      setTimeout(() => {
        router.push("/files");
      }, 3000);
      // router.push("/files");
      return response.data;
    } catch (err) {
      console.log("13V", err);
      // toast.error("Unable to Create with provided credentials.");
      return rejectWithValue(err.response.data);
    }
  }
);

export const fileUpdateStore = createAsyncThunk(
  "file/createzzz/",
  async ({ formData, toast, router, id }, { rejectWithValue }) => {
    try {
      const response = await API.put(`files/${id}/`, formData);
      toast.success("Updated Successfully");
      setTimeout(() => {
        router.push("/files");
      }, 3000);
      // router.push("/files");
      return response.data;
    } catch (err) {
      console.log("13V", err);
      // toast.error("Unable to Create with provided credentials.");
      return rejectWithValue(err.response.data);
    }
  }
);

export const fileAssign = createAsyncThunk(
  "file/createzzz/",
  async ({ formData, toast, router, id }, { rejectWithValue }) => {
    try {
      const response = await API.put(`assign-agent/${id}/`, formData);
      toast.success("File Assigned Successfully");
      router.push("/files/" + id);
      return response.data;
    } catch (err) {
      console.log("13V", err);
      // toast.error("Unable to Create with provided credentials.");
      return rejectWithValue(err.response.data);
    }
  }
);

export const verifyCreate = createAsyncThunk(
  "verify/createcc/",
  async ({ formData, toast, router, id }, { rejectWithValue }) => {
    try {
      const response = await API.post("verify/create/", formData);
      toast.success("Created Successfully");
      router.push("/files/" + id);
      return response.data;
    } catch (err) {
      //   console.log("13", err);
      toast.error("Unable to Create with provided credentials.");
      return rejectWithValue(err.response.data);
    }
  }
);

export const verifyDelete = createAsyncThunk(
  "verify/delete/",
  async ({ toast, router, id_v, id }, { rejectWithValue }) => {
    try {
      const response = await API.delete(`verify/delete/${id_v}/`);
      toast.success("Deleted Successfully");
      router.reload("/files/" + id);
      return response.data;
    } catch (err) {
      //   console.log("13", err);
      toast.error("Unable to Delete with provided credentials.");
      return rejectWithValue(err.response.data);
    }
  }
);



const fileSlice = createSlice({
  name: "files",
  initialState: initialState,
  // reducers: {
  //   getUserId: function (state, action) {
  //     state.user = action.payload;
  //   },
  // },
  extraReducers: (builder) => {
    // Add reducers for additional action types here, and handle loading state as needed
    builder
      .addCase(getFiles.pending, (state, action) => {
        state.loading = true;
      })
      .addCase(getFiles.fulfilled, (state, action) => {
        state.loading = false;
        state.files = action.payload?.files;
        state.unassigned_files = action.payload?.unassigned_files;
        state.file_num = action.payload?.fileNum;
        state.profile_id = action.payload?.user_profile;
      })
      .addCase(getFiles.rejected, (state, action) => {
        state.loading = false;
        state.error = `Oops! Something is wrong with the Server!`;
      })
      .addCase(getFilesById.pending, (state, action) => {
        state.loading = true;
      })
      .addCase(getFilesById.fulfilled, (state, action) => {
        state.loading = false;
        state.fileById = action.payload.files;
        state.verifyy = action.payload.verify;
      })
      .addCase(getFilesById.rejected, (state, action) => {
        state.loading = false;
        state.error = `Oops! Something went wrong! Go back to file`;
      })
      .addCase(getAgent.pending, (state, action) => {
        state.loading = true;
      })
      .addCase(getAgent.fulfilled, (state, action) => {
        state.loading = false;
        state.users = action.payload;
      })
      .addCase(getAgent.rejected, (state, action) => {
        state.loading = false;
        state.error = `Oops! Something went wrong! Go back to file`;
      })
      .addCase(deleteFilesById.pending, (state, action) => {
        state.loading = true;
      })
      .addCase(deleteFilesById.fulfilled, (state, action) => {
        state.loading = false;
        // state.users = action.payload;
      })
      .addCase(deleteFilesById.rejected, (state, action) => {
        state.loading = false;
        state.error = `Oops! Something went wrong! Go back to file`;
      });
  },
});

// export const { getUserId } = fileSlice.actions;
export default fileSlice.reducer;
