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
    stats: Stats;
    meta: Meta;
    entities: Record<string, any>;
    collections: Record<string, any[]>;
    uid: string;
    display_name: string;
    description: string;
}

interface Player extends BaseEntity {
    __type: 'Player';
}

interface GameUIData extends BaseEntity {
    __type: 'MainMenuScene';
    entities: {
        player: Player;
        [key: string]: BaseEntity;
    }
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
            {/* Title Section */}
            <div className="flex-1 flex items-center justify-center">
                <h1 className="text-6xl font-bold text-white tracking-wider">
                    {props.data.display_name || "CREATURE GAME"}
                </h1>
            </div>

            {/* Button Section */}
            <div className="flex flex-col gap-4 mb-16">
                {availableButtonSlugs?.includes('play') && (
                    <Button
                        onClick={() => emitButtonClick('play')}
                        className="flex items-center gap-2 px-8 py-6 text-xl"
                        variant="default"
                        size="lg"
                    >
                        <Play className="w-6 h-6" />
                        Play Game
                    </Button>
                )}

                {availableButtonSlugs?.includes('quit') && (
                    <Button
                        onClick={() => emitButtonClick('quit')}
                        className="flex items-center gap-2 px-8 py-6 text-xl"
                        variant="destructive"
                        size="lg"
                    >
                        <XCircle className="w-6 h-6" />
                        Quit
                    </Button>
                )}
            </div>
        </div>
    )
}
