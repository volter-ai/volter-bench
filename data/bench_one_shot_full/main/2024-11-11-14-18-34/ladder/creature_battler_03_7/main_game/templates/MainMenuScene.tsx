import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Play, Power} from 'lucide-react'

interface ExamplePlayer {
    uid: string;
    stats: {
        stat1: number;
    };
    meta?: {
        prototype_id: string;
        category: string;
    };
    collections?: {
        creatures?: Array<{
            uid: string;
            stats: {
                hp: number;
                max_hp: number;
                attack: number;
                defense: number;
                speed: number;
            };
            meta: {
                prototype_id: string;
                category: string;
                creature_type: string;
            };
        }>;
    };
    display_name: string;
    description: string;
}

interface GameUIData {
    entities: {
        player: ExamplePlayer;
    };
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    return (
        <div className="relative w-full" style={{ aspectRatio: '16/9' }}>
            <div className="absolute inset-0 bg-gradient-to-b from-blue-900 to-blue-950 flex flex-col justify-between items-center p-8">
                <div className="flex-1 flex items-center justify-center">
                    <h1 className="text-6xl font-bold text-white tracking-wider">
                        {props.data?.entities?.player?.display_name || "Game Title"}
                    </h1>
                </div>

                <div className="flex flex-col gap-4 mb-16">
                    {availableButtonSlugs.includes('play') && (
                        <button
                            onClick={() => emitButtonClick('play')}
                            className="flex items-center gap-2 px-8 py-4 bg-green-600 hover:bg-green-700 text-white rounded-lg text-xl transition-colors"
                        >
                            <Play size={24} />
                            Play Game
                        </button>
                    )}

                    {availableButtonSlugs.includes('quit') && (
                        <button
                            onClick={() => emitButtonClick('quit')}
                            className="flex items-center gap-2 px-8 py-4 bg-red-600 hover:bg-red-700 text-white rounded-lg text-xl transition-colors"
                        >
                            <Power size={24} />
                            Quit
                        </button>
                    )}
                </div>
            </div>
        </div>
    )
}
