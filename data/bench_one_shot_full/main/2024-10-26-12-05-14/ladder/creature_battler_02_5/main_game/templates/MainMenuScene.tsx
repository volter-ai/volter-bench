import React, { useCallback } from "react";
import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';
import { Button } from "@/components/ui/button";

interface ExamplePlayer {
    uid: string,
    stats: {
        stat1: number,
    },
}

interface GameUIData {
    entities: {
        player: ExamplePlayer
    }
}

const renderButtons = (availableButtonSlugs: string[], emitButtonClick: (slug: string) => void) => {
    return (
        <div className="flex flex-col space-y-4">
            {availableButtonSlugs.includes('play') && (
                <Button
                    onClick={() => emitButtonClick('play')}
                    className="w-48"
                >
                    <Play className="mr-2 h-4 w-4" /> Play Game
                </Button>
            )}
            {availableButtonSlugs.includes('quit') && (
                <Button
                    onClick={() => emitButtonClick('quit')}
                    variant="destructive"
                    className="w-48"
                >
                    <X className="mr-2 h-4 w-4" /> Quit Game
                </Button>
            )}
        </div>
    );
};

export const MainMenuSceneView = React.memo(function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    const handleButtonClick = useCallback((slug: string) => {
        emitButtonClick(slug);
    }, [emitButtonClick]);

    return (
        <div className="w-full h-full flex items-center justify-center bg-gray-900">
            <div className="w-full h-full max-w-screen-lg mx-auto aspect-video bg-gradient-to-b from-blue-900 to-blue-700 flex flex-col items-center justify-between p-8">
                <h1 className="text-4xl md:text-6xl font-bold text-white mt-16">
                    Game Title
                </h1>
                <div className="flex-grow" />
                {renderButtons(availableButtonSlugs, handleButtonClick)}
            </div>
        </div>
    );
});
