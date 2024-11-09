import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react'
import { Button } from "@/components/ui/button"

interface Stats {
    hp?: number;
    max_hp?: number;
    attack?: number;
    defense?: number;
    sp_attack?: number;
    sp_defense?: number;
    speed?: number;
    [key: string]: number | undefined;
}

interface Meta {
    prototype_id: string;
    category: string;
    [key: string]: string;
}

interface BaseEntity {
    __type: string;
    uid: string;
    stats: Stats;
    meta: Meta;
    entities: Record<string, any>;
    collections: Record<string, any[]>;
    display_name: string;
    description: string;
}

interface Player extends BaseEntity {
    __type: 'Player';
}

interface GameUIData {
    entities: {
        player: Player;
    }
    stats: Record<string, number>;
    meta: Record<string, string>;
    collections: Record<string, any[]>;
    uid: string;
    display_name: string;
    description: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    if (!props.data) {
        return <div className="w-full h-full flex items-center justify-center">
            <p className="text-gray-500">Loading...</p>
        </div>
    }

    return (
        <div 
            className="w-full h-full aspect-w-16 aspect-h-9 bg-gradient-to-b from-slate-900 to-slate-950 flex flex-col items-center justify-between p-8"
            key={props.data.uid}
        >
            <div className="flex-1 flex items-center justify-center">
                <h1 className="text-6xl font-bold text-white tracking-wider">
                    {props.data.display_name || "CREATURE GAME"}
                </h1>
            </div>

            <div className="flex flex-col gap-4 mb-16">
                {availableButtonSlugs?.includes('play') && (
                    <Button
                        onClick={() => emitButtonClick('play')}
                        className="w-48 h-14 text-lg"
                        variant="default"
                    >
                        <Play className="w-5 h-5 mr-2" />
                        Play Game
                    </Button>
                )}

                {availableButtonSlugs?.includes('quit') && (
                    <Button
                        onClick={() => emitButtonClick('quit')}
                        className="w-48 h-14 text-lg"
                        variant="destructive"
                    >
                        <XCircle className="w-5 h-5 mr-2" />
                        Quit
                    </Button>
                )}
            </div>
        </div>
    )
}
