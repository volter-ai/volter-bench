import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react';
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

    return (
        <div className="relative w-full h-full aspect-video bg-gradient-to-b from-slate-800 to-slate-900 flex flex-col items-center justify-between p-8">
            {/* Title Section */}
            <div className="flex-1 flex items-center justify-center w-full">
                <h1 className="text-6xl font-bold text-white tracking-wider">
                    {props?.data?.entities?.player?.uid || "Game Title"}
                </h1>
            </div>

            {/* Button Container */}
            <div className="flex flex-col gap-4 w-full max-w-md mb-8">
                {availableButtonSlugs.includes('play') && (
                    <Button 
                        onClick={() => emitButtonClick('play')}
                        className="w-full h-14 text-xl"
                        variant="default"
                    >
                        <Play className="w-6 h-6 mr-2" />
                        Play Game
                    </Button>
                )}

                {availableButtonSlugs.includes('quit') && (
                    <Button
                        onClick={() => emitButtonClick('quit')}
                        className="w-full h-14 text-xl"
                        variant="destructive"
                    >
                        <XCircle className="w-6 h-6 mr-2" />
                        Quit
                    </Button>
                )}
            </div>
        </div>
    );
}
