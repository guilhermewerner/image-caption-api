import Head from 'next/head'
import { Inter } from 'next/font/google'
import styles from '@/styles/Home.module.css'

import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Image from 'react-bootstrap/Image';
import Ratio from 'react-bootstrap/Ratio';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { useState } from 'react';

export default function Home() {
    const [image64, setImage64] = useState<string | ArrayBuffer | null | undefined>(null);
    const [imageUrl, setImageUrl] = useState<string | ArrayBuffer | null | undefined>(null);
    const [caption, setCaption] = useState<string | null | undefined>(null);

    const handleImageChange = (e: any) => {
        const file = e.target.files[0];

        if (file) {
            const imageUrl = URL.createObjectURL(file);
            setImageUrl(imageUrl);

            const reader = new FileReader();

            reader.onload = (e) => {
                const base64Image = e?.target?.result;
                setImage64(base64Image);
            };

            reader.readAsDataURL(file);
        }
    };

    const handleSubmit = () => {
        if (imageUrl) {
            fetch("https://ti6.fornaxhost.net/caption-base64", {
                method: "POST",
                body: JSON.stringify({ image_base64: image64 }),
                headers: {
                    "Content-Type": "application/json",
                }
            }).then((res) => {
                if (res.status === 200) {
                    return res.json();
                }
            }).then((data) => {
                setCaption(data.caption)
            })
        }
    };

    return (
        <>
            <Head>
                <title>Image Caption</title>
            </Head>
            <div className='wrapper'>
                <header>
                    <Navbar expand="lg" className="main-nav shadow-sm">
                        <Container>
                            <Navbar.Brand href="/">Image Caption</Navbar.Brand>
                        </Container>
                    </Navbar>
                </header>
                <main className='mt-3'>
                    <Container>
                        <p className="mb-2">Envie uma imagem para obter sua descrição.</p>
                        <Form className='my-3'>
                            <Form.Group className="mb-3">
                                <Form.Label>Imagem</Form.Label>
                                <div className='d-flex justify-content-center align-items-center flex-grow-1'>
                                    <div
                                        className='d-flex'
                                        style={{ width: '720px', height: '100%' }}
                                    >
                                        <Ratio className='d-flex' aspectRatio="16x9">
                                            <Image src={imageUrl as string} />
                                        </Ratio>
                                    </div>
                                </div>
                            </Form.Group>
                            <Form.Group className="mb-3" controlId="formUpload">
                                <Form.Label>Enviar imagem</Form.Label>
                                <Form.Control type="file" onChange={handleImageChange} />
                            </Form.Group>
                            <Form.Group className="mb-3" controlId="formCaption">
                                <Form.Label>Descrição</Form.Label>
                                <Form.Control type="text" disabled value={caption ? caption : ""} />
                            </Form.Group>
                            <div className='text-end'>
                                <Button variant="primary" onClick={handleSubmit}>
                                    Enviar
                                </Button>
                            </div>
                        </Form>
                    </Container>
                </main>
                <footer>
                    <Container className="mb-2 pb-2">
                        <span className="text-muted">Feito por</span>
                    </Container>
                </footer>
            </div>
        </>
    )
}
