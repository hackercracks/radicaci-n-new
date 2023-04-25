import Link from "next/link";
import { useEffect } from "react";
import { useRouter } from "next/router";
import Layout from "@/components/Layout";

const NotFound = () => {
  const router = useRouter();

  useEffect(() => {
    setTimeout(() => {
      router.push("/files");
    }, 3000);
  }, []);

  return (
    <div className="container text-center mt-5">
      <h1>Ooops...</h1>
      <h2>esa pagina no se encuentra :(</h2>
      <p>
        Volviendo a la{" "}
        <Link href="/">
          Página principal
        </Link>
        son 3 segundos...
      </p>
    </div>
  );
};

export default NotFound;
