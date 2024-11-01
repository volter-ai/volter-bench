import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Play, X } from 'lucide-react';

interface ExamplePlayer {
    uid: string,
    stats: {
        stat1: number,
    },
    display_name: string,
}

interface GameUIData {
    entities: {
        player: ExamplePlayer
    },
    stats: Record<string, any>,
    meta: Record<string, any>,
    collections: Record<string, any>,
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    const playerName = props.data.entities.player?.display_name || "Player";

    return (
        <div className="w-full h-full bg-gradient-to-b from-blue-500 to-purple-600 flex flex-col items-center justify-between p-8">
            <Card className="w-full text-center py-8 bg-opacity-80 bg-white">
                <h1 className="text-6xl font-bold text-blue-800">Creature Battle Game</h1>
            </Card>

            <div className="text-2xl text-white">
                Welcome, {playerName}!
            </div>

            <Card className="w-full max-w-md p-6 bg-opacity-80 bg-white">
                <div className="flex flex-col space-y-4">
                    {availableButtonSlugs.includes('play') && (
                        <Button
                            onClick={() => emitButtonClick('play')}
                            className="w-full text-xl py-6"
                        >
                            <Play className="mr-2" /> Play Game
                        </Button>
                    )}
                    {availableButtonSlugs.includes('quit') && (
                        <Button
                            onClick={() => emitButtonClick('quit')}
                            variant="destructive"
                            className="w-full text-xl py-6"
                        >
                            <X className="mr-2" /> Quit Game
                        </Button>
                    )}
                </div>
            </Card>
        </div>
    );
}
