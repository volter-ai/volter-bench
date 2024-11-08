import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';
import { Button } from "@/components/ui/button";

interface GameStats {
    [key: string]: number;
}

interface GameMeta {
    prototype_id: string;
    category: string;
}

interface GameUIData {
    entities: {
        player: {
            uid: string,
            stats: GameStats,
            meta: GameMeta,
            collections: {
                creatures: Array<{
                    uid: string;
                    stats: GameStats;
                    meta: GameMeta;
                }>
            }
        }
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
                <div className="flex-1 flex items-center justify-center">
                    <div className="w-96 h-32 bg-contain bg-center bg-no-repeat" 
                         style={{ backgroundImage: 'url(/game-title.png)' }}>
                    </div>
                </div>

                {/* Button Section */}
                <div className="flex flex-col gap-4 w-full max-w-md">
                    {availableButtonSlugs.includes('play') && (
                        <Button 
                            variant="default"
                            size="lg"
                            className="w-full text-xl"
                            onClick={() => emitButtonClick('play')}
                        >
                            <Play className="mr-2 h-5 w-5" />
                            Play Game
                        </Button>
                    )}

                    {availableButtonSlugs.includes('quit') && (
                        <Button
                            variant="destructive"
                            size="lg"
                            className="w-full text-xl"
                            onClick={() => emitButtonClick('quit')}
                        >
                            <X className="mr-2 h-5 w-5" />
                            Quit
                        </Button>
                    )}
                </div>
            </div>
        </div>
    );
}
