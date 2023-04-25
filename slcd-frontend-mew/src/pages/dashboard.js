import Layout from '@/components/Layout';
import axios from 'axios';
import { useRouter } from 'next/router';
import { useEffect } from 'react';
import {
  MdOutlineNotificationsNone,
  MdInventory2,
  MdBookmarkRemove,
  MdOutlineMarkChatRead,
  MdOutlineArchive,
} from "react-icons/md";
import { useSelector } from 'react-redux';



const Dashboard = () => {
  const { files, unassigned_files } = useSelector(
    (stateData) => ({
      ...stateData.files,
    })
  );

   const {is_organisor } = useSelector(
     (stateData) => ({
       ...stateData.auth,
     })
  );

  const router = useRouter();
  
  useEffect(() => {
    if (!is_organisor) {
      router.push("/files")
    }
  },[])

  // console.log("sis beh", files?.length + unassigned_files?.length)
return (
  <Layout>
    <div className="px-4">
      <div className="main-title">
        <p className="fw-bold">PANEL PRINCIPAL</p>
      </div>

      <div className="main-cards">
        <div className="card">
          <div className="card-inner">
            <p className="text-secondary">Total de tramites</p>
            <MdInventory2 />
          </div>
          <span className="text-secondary fw-bold">
            {files?.length + unassigned_files?.length}
          </span>
        </div>

        <div className="card">
          <div className="card-inner">
            <p className="text-secondary">Sin asignar</p>
            <MdBookmarkRemove />
          </div>
          <span className="text-secondary fw-bold">
            {unassigned_files?.length}
          </span>
        </div>

        <div className="card">
          <div className="card-inner">
            <p className="text-secondary">Asignados</p>
            <MdOutlineMarkChatRead />
          </div>
          <span className="text-secondary fw-bold">
            {files?.length}
          </span>
        </div>

        <div className="card">
          <div className="card-inner">
            <p className="text-secondary">Archivados</p>
            <MdOutlineArchive />
          </div>
          <span className="text-secondary fw-bold">0</span>
        </div>
      </div>
    </div>
  </Layout>
);
}

export default Dashboard