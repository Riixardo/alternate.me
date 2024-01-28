import React, { useState } from 'react';
import { MouseEvent } from 'react';

interface Props {
    arr: string[]
    heading: string
    onSelectItem: (item: string) => void
}

function ListGroup({arr, heading, onSelectItem} :Props) {

    // const handleClick = (e: MouseEvent) => console.log(e);
    const [selectedIndex, setSelectedIndex] = useState(-1);

    return (
    <>
        <h1>{heading}</h1>
        <ul className="list-group">
            {arr.map((item, idx) => <li className={(selectedIndex === idx ? 'list-group-item active' : 'list-group-item')}
            key={item} onClick={() => {setSelectedIndex(idx); onSelectItem(item)}}>{item}</li>)}
        </ul>
    </>
    );
}

export default ListGroup;
