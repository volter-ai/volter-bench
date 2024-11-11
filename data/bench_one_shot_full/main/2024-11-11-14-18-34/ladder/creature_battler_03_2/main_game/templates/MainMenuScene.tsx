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
            stats: Record<string, number>;
            meta: Record<string, string>;
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

type ButtonSlug = 'play' | 'quit';

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    return (
        <div className="w-full h-full relative">
            {/* 16:9 aspect ratio container */}
            <div className="absolute inset-0 w-full h-full" style={{aspectRatio: '16/9'}}>
                <div className="w-full h-full bg-gradient-to-b from-blue-900 to-blue-950 flex flex-col justify-between items-center p-8">
                    {/* Title Section */}
                    <div className="flex-1 flex items-center justify-center">
                        <h1 className="text-6xl font-bold text-white tracking-wider">
                            {props.data?.entities?.player?.display_name || "Creature Game"}
                        </h1>
                    </div>

                    {/* Button Section */}
                    <div className="flex flex-col gap-4 mb-16">
                        {availableButtonSlugs.includes('play') && (
                            <button
                                onClick={() => emitButtonClick('play' as ButtonSlug)}
                                className="flex items-center justify-center gap-2 px-8 py-4 bg-green-600 hover:bg-green-700 text-white rounded-lg text-xl transition-colors min-w-[200px]"
                            >
                                <Play className="w-6 h-6" />
                                <span>Play Game</span>
                            </button>
                        )}

                        {availableButtonSlugs.includes('quit') && (
                            <button
                                onClick={() => emitButtonClick('quit' as ButtonSlug)}
                                className="flex items-center justify-center gap-2 px-8 py-4 bg-red-600 hover:bg-red-700 text-white rounded-lg text-xl transition-colors min-w-[200px]"
                            >
                                <Power className="w-6 h-6" />
                                <span>Quit</span>
                            </button>
                        )}
                    </div>
                </div>
            </div>
        </div>
    )
}
