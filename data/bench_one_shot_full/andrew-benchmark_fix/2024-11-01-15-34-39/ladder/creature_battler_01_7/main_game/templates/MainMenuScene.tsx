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
    } = useCurrentButtons()

    const player = props.data.entities.player;

    return (
        <div className="w-full h-full bg-gradient-to-b from-blue-500 to-blue-700 flex flex-col items-center justify-between p-8" style={{ aspectRatio: '16/9' }}>
            <div className="text-6xl font-bold text-white mt-16">Game Title</div>
            
            <div className="text-2xl text-white">
                Welcome, {player?.display_name || "Player"}!
            </div>
            
            <div className="flex flex-col items-center space-y-4 mb-16">
                {availableButtonSlugs.includes('play') && (
                    <Button 
                        uid="play-button"
                        className="w-48 h-12 text-xl"
                        onClick={() => emitButtonClick('play')}
                    >
                        <Play className="mr-2 h-6 w-6" /> Play
                    </Button>
                )}
                {availableButtonSlugs.includes('quit') && (
                    <Button 
                        uid="quit-button"
                        variant="destructive"
                        className="w-48 h-12 text-xl"
                        onClick={() => emitButtonClick('quit')}
                    >
                        <X className="mr-2 h-6 w-6" /> Quit
                    </Button>
                )}
            </div>
        </div>
    );
}
