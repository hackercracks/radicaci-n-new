import React, { useEffect, useState } from "react";
import Layout from "@/components/Layout";
import DataTable from "react-data-table-component";
import { AiFillDelete, AiFillEdit } from "react-icons/ai";
import { useSelector, useDispatch } from "react-redux";
import { getAgent, getFiles } from "@/redux/features/fileSlice";
import Link from "next/link";

const Agent = () => {
  const { loading, error, files, users } = useSelector(
    (stateData) => ({
      ...stateData.files,
    })
  );

  const column = [
    {
      name: "Titular",
      selector: (row) => row.user.email,
      sortable: true,
    },
    {
      name: "Start Date",
      selector: (row) => row.user.username,
      sortable: true,
    },
    {
      name: "Phone Number",
      cell: (row) => (
        <div>
          {row.user.is_agent && "responsable"}
          {row.user.is_support && "Atención al cliente"}
        </div>
      ),
      sortable: true,
    },
    {
      name: "Action",
      cell: (row) => (
        <div>
          <span className="badge bg-danger border-0 fs-6 mx-1">
            <AiFillDelete />
          </span>
        </div>
      ),
    },
  ];

  const customStyles = {
    headRow: {
      style: {
        backgroundColor: "blue",
        color: "white",
      },
    },
    headCell: {
      style: {
        fontSize: "16px",
        fontWeight: "600",
        textTransform: "uppercase",
      },
    },
    cells: {
      style: {
        fontSize: "15px",
      },
    },
  };

  let dispatch = useDispatch();

  useEffect(() => {
    dispatch(getFiles());

    dispatch(getAgent());
  }, [dispatch]);

  console.log("aqwr", users)

  return (
    <Layout>
      <div className="container px-3">
        {loading && (
          <div className="spinner-border" role="status">
            <span className="visually-hidden">Cargando...</span>
          </div>
        )}
        {!loading && error?.length > 0 && (
          <h3 className="text-danger text-center mt-5">{error}</h3>
        )}
        {!loading && users?.length > 0 && (
          <DataTable
            title="Agent List"
            columns={column}
            data={users}
            customStyles={customStyles}
            pagination
            selectableRows
            selectableRowsHighlight
            highlightOnHover
            fixedHeader
            fixedHeaderScrollHeight="400px"
          ></DataTable>
        )}
      </div>
    </Layout>
  );
};

export default Agent;
