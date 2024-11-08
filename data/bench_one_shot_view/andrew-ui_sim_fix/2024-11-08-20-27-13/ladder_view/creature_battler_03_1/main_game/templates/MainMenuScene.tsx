import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Play, Power} from 'lucide-react';
import {Button} from "@/components/ui/button";

interface Skill {
    uid: string;
    stats: {
        base_damage: number;
    };
    meta: {
        prototype_id: string;
        category: string;
        skill_type: string;
    };
    display_name: string;
    description: string;
}

interface Creature {
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
    collections: {
        skills: Skill[];
    };
    display_name: string;
    description: string;
}

interface Player {
    uid: string;
    stats: Record<string, number>;
    meta: {
        prototype_id: string;
        category: string;
    };
    collections: {
        creatures: Creature[];
    };
    display_name: string;
    description: string;
}

interface GameUIData {
    uid: string;
    __type: string;
    stats: Record<string, unknown>;
    meta: Record<string, unknown>;
    entities: {
        player: Player;
    };
    collections: Record<string, unknown>;
    display_name: string;
    description: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    return (
        <div 
            className="relative w-full h-0 pb-[56.25%] bg-gradient-to-b from-slate-900 to-slate-800"
            key={props.data.uid}
        >
            <div className="absolute inset-0 flex flex-col items-center justify-between p-8">
                {/* Title Section */}
                <div className="flex-1 flex items-center justify-center">
                    <div className="relative w-96 h-32 bg-center bg-contain bg-no-repeat">
                        <h1 className="text-6xl font-bold text-white tracking-wider text-center">
                            {props.data.display_name || "GAME TITLE"}
                        </h1>
                    </div>
                </div>

                {/* Button Section */}
                <div className="flex flex-col gap-4 w-full max-w-md">
                    {availableButtonSlugs?.includes('play') && (
                        <Button
                            onClick={() => emitButtonClick('play')}
                            className="w-full py-6 bg-emerald-600 hover:bg-emerald-500 text-xl"
                        >
                            <Play className="w-6 h-6 mr-2" />
                            Play Game
                        </Button>
                    )}

                    {availableButtonSlugs?.includes('quit') && (
                        <Button
                            onClick={() => emitButtonClick('quit')}
                            variant="destructive"
                            className="w-full py-6 text-xl"
                        >
                            <Power className="w-6 h-6 mr-2" />
                            Quit
                        </Button>
                    )}
                </div>
            </div>
        </div>
    )
}
