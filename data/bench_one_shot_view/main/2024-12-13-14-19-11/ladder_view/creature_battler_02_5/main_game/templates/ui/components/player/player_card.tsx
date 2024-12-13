import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

interface BasePlayerCardProps extends React.ComponentProps<typeof Card> {
  uid: string
  name: string
  imageUrl: string
}

let BasePlayerCard = React.forwardRef<HTMLDivElement, BasePlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <Card ref={ref} className={cn("w-[350px]", className)} uid={uid} {...props}>
      <CardHeader uid={uid}>
        <CardTitle uid={uid}>{name}</CardTitle>
      </CardHeader>
      <CardContent uid={uid}>
        <img
          src={imageUrl}
          alt={name}
          className="w-full h-[200px] object-cover rounded-md"
        />
      </CardContent>
    </Card>
  )
)

BasePlayerCard.displayName = "BasePlayerCard"

let PlayerCard = withClickable(BasePlayerCard)

export { PlayerCard }
