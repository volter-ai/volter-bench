import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card,
  CardHeader,
  CardContent,
  CardFooter,
  CardTitle,
} from "@/components/ui/card"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  hp: number
  maxHp: number
  imageUrl: string
}

let CreatureCardRoot = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, maxHp, imageUrl, ...props }, ref) => (
    <Card 
      ref={ref} 
      className={cn("w-[300px]", className)} 
      uid={uid}
      {...props}
    >
      <CardHeader uid={`${uid}-header`}>
        <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
      </CardHeader>
      <CardContent uid={`${uid}-content`}>
        <img 
          src={imageUrl}
          alt={name}
          className="w-full h-48 object-contain"
        />
        <div className="mt-4">
          <div className="flex justify-between">
            <span>HP:</span>
            <span>{hp}/{maxHp}</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2.5">
            <div 
              className="bg-green-600 h-2.5 rounded-full" 
              style={{width: `${(hp/maxHp) * 100}%`}}
            />
          </div>
        </div>
      </CardContent>
    </Card>
  )
)

CreatureCardRoot.displayName = "CreatureCard"

let CreatureCard = withClickable(CreatureCardRoot)

export { CreatureCard }
