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

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    const playerName = props.data?.entities?.player?.uid || "Player";

    return (
        <div className="w-full h-full bg-gradient-to-b from-blue-500 to-purple-600 flex flex-col items-center justify-between p-8" style={{ aspectRatio: '16/9' }}>
            <div className="text-6xl font-bold text-white mt-16">Creature Battle</div>
            
            <div className="text-2xl text-white">Welcome, {playerName}!</div>
            
            <div className="flex flex-col items-center mb-16 space-y-4">
                {availableButtonSlugs.includes('play') && (
                    <Button 
                        onClick={() => emitButtonClick('play')}
                        className="w-48 h-12 text-xl"
                        uid="play-button"
                    >
                        <Play className="mr-2 h-6 w-6" /> Play
                    </Button>
                )}
                {availableButtonSlugs.includes('quit') && (
                    <Button 
                        onClick={() => emitButtonClick('quit')}
                        className="w-48 h-12 text-xl"
                        variant="destructive"
                        uid="quit-button"
                    >
                        <X className="mr-2 h-6 w-6" /> Quit
                    </Button>
                )}
            </div>
        </div>
    );
}
