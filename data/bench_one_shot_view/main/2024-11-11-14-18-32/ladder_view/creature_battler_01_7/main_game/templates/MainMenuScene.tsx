import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

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
        <div className="relative w-full" style={{ paddingBottom: '56.25%' }}>
            <div className="absolute inset-0 flex flex-col items-center justify-between p-8 bg-gradient-to-b from-slate-900 to-slate-800">
                {/* Title Image Section */}
                <div className="flex-1 flex items-center justify-center w-full">
                    <Card className="w-full max-w-2xl bg-transparent border-none shadow-none">
                        <div className="w-full h-48 bg-contain bg-center bg-no-repeat" 
                             style={{ backgroundImage: "url('/game-title.png')" }} 
                             role="img" 
                             aria-label="Game Title" />
                    </Card>
                </div>

                {/* Button Section */}
                <Card className="w-full max-w-md bg-transparent border-none shadow-none">
                    <div className="flex flex-col gap-4">
                        {availableButtonSlugs?.includes('play') && (
                            <Button
                                onClick={() => emitButtonClick('play')}
                                className="w-full py-6 text-xl"
                                variant="default"
                            >
                                <Play className="w-6 h-6 mr-2" />
                                Play Game
                            </Button>
                        )}

                        {availableButtonSlugs?.includes('quit') && (
                            <Button
                                onClick={() => emitButtonClick('quit')}
                                className="w-full py-6 text-xl"
                                variant="destructive"
                            >
                                <XCircle className="w-6 h-6 mr-2" />
                                Quit
                            </Button>
                        )}
                    </div>
                </Card>
            </div>
        </div>
    );
}
