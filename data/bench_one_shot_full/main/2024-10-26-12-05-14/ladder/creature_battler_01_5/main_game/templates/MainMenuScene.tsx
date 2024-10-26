import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';
import { Button } from "@/components/ui/button";

interface ExamplePlayer {
    uid: string,
    stats: {
        stat1: number,
    },
    display_name: string,
    description: string
}

interface GameUIData {
    entities: {
        player: ExamplePlayer
    }
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons();

    const player = props.data.entities.player;
    const playerName = player?.display_name || "Default Player";

    return (
        <div className="w-full h-full bg-blue-500 flex flex-col items-center justify-between p-8" style={{ aspectRatio: '16/9' }}>
            <div className="text-6xl font-bold text-white mt-16">Game Title</div>
            
            <div className="text-2xl text-white">
                Welcome, {playerName}!
            </div>
            
            <div className="flex flex-col items-center space-y-4 mb-16">
                {availableButtonSlugs.includes('play') && (
                    <Button 
                        className="w-48 h-12 text-xl bg-gray-800 hover:bg-gray-700"
                        onClick={() => emitButtonClick('play')}
                    >
                        <Play className="mr-2 h-6 w-6" /> Play
                    </Button>
                )}
                {availableButtonSlugs.includes('quit') && (
                    <Button 
                        className="w-48 h-12 text-xl bg-red-500 hover:bg-red-600"
                        onClick={() => emitButtonClick('quit')}
                    >
                        <X className="mr-2 h-6 w-6" /> Quit
                    </Button>
                )}
            </div>
        </div>
    );
}
